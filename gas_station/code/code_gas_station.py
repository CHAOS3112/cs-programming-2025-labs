import json
import os
from datetime import datetime
from typing import List, Dict, Optional



# Классы данных


class FuelType:
    AI92 = "АИ-92"
    AI95 = "АИ-95"
    AI98 = "АИ-98"
    DT = "ДТ"


class Tank:
    def __init__(self, fuel_type: str, tank_id: int, max_volume: int, min_level: int = 2000):
        self.fuel_type = fuel_type
        self.tank_id = tank_id
        self.max_volume = max_volume
        self.current_volume = max_volume  # полные цистерны
        self.min_level = min_level
        self.enabled = True

    def is_low(self) -> bool:
        return self.current_volume < self.min_level

    def disable_if_low(self):
        if self.is_low():
            self.enabled = False

    def can_supply(self, liters: int) -> bool:
        return self.enabled and self.current_volume >= liters

    def withdraw(self, liters: int):
        if self.can_supply(liters):
            self.current_volume -= liters
            self.disable_if_low()
        else:
            raise ValueError("Недостаточно топлива или цистерна отключена")

    def refill(self, liters: int):
        if self.current_volume + liters > self.max_volume:
            raise ValueError("Превышение максимального объема")
        self.current_volume += liters

    def to_dict(self):
        return {
            "fuel_type": self.fuel_type,
            "tank_id": self.tank_id,
            "max_volume": self.max_volume,
            "current_volume": self.current_volume,
            "min_level": self.min_level,
            "enabled": self.enabled
        }

    @classmethod
    def from_dict(cls, data):
        tank = cls(data["fuel_type"], data["tank_id"], data["max_volume"], data["min_level"])
        tank.current_volume = data["current_volume"]
        tank.enabled = data["enabled"]
        return tank

    def __str__(self):
        status = "ВКЛ" if self.enabled else "ВЫКЛ"
        extra = f" (ниже порога)" if not self.enabled and self.is_low() else ""
        return f"{self.fuel_type} №{self.tank_id} | {self.current_volume} / {self.max_volume} л | {status}{extra}"


class Nozzle:
    def __init__(self, fuel_type: str, tank: Tank):
        self.fuel_type = fuel_type
        self.tank = tank

    def is_available(self) -> bool:
        return self.tank.enabled

    def get_tank_info(self) -> str:
        return f"{self.fuel_type} №{self.tank.tank_id}"


class Pump:
    def __init__(self, pump_id: int, nozzles: List[Nozzle]):
        self.pump_id = pump_id
        self.nozzles = nozzles

    def get_available_fuels(self) -> List[Nozzle]:
        return [n for n in self.nozzles if n.is_available()]

    def get_all_fuels(self) -> List[Nozzle]:
        return self.nozzles

    def __str__(self):
        fuels = ", ".join([n.fuel_type for n in self.nozzles])
        return f"Колонка {self.pump_id}: {fuels}"


class Operation:
    def __init__(self, op_type: str, details: str, timestamp: str = None):
        self.op_type = op_type
        self.details = details
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {"op_type": self.op_type, "details": self.details, "timestamp": self.timestamp}

    @classmethod
    def from_dict(cls, data):
        return cls(data["op_type"], data["details"], data["timestamp"])

    def __str__(self):
        return f"[{self.timestamp}] {self.op_type}: {self.details}"


# Основной класс системы АЗС


class GasStation:
    FUEL_PRICES = {
        FuelType.AI92: 57.50,
        FuelType.AI95: 58.30,
        FuelType.AI98: 61.20,
        FuelType.DT: 54.80
    }

    def __init__(self):
        self.tanks: List[Tank] = []
        self.pumps: List[Pump] = []
        self.operations: List[Operation] = []
        self.stats = {
            "total_income": 0.0,
            "cars_served": 0,
            "fuel_sold": {ft: 0 for ft in [FuelType.AI92, FuelType.AI95, FuelType.AI98, FuelType.DT]},
            "fuel_income": {ft: 0.0 for ft in [FuelType.AI92, FuelType.AI95, FuelType.AI98, FuelType.DT]}
        }
        self.emergency_mode = False
        self._init_default_setup()

    def _init_default_setup(self):
        # цистерны
        self.tanks = [
            Tank(FuelType.AI92, 1, 20000),
            Tank(FuelType.AI95, 1, 20000),
            Tank(FuelType.AI95, 2, 20000),
            Tank(FuelType.AI98, 1, 15000),
            Tank(FuelType.DT, 1, 25000)
        ]

        # Связь колонки с цистернами
        tank_map = {(t.fuel_type, t.tank_id): t for t in self.tanks}

        # Схема подключения
        pump_config = {
            1: [FuelType.AI92, FuelType.AI95],
            2: [FuelType.AI92, FuelType.AI95],
            3: [FuelType.AI92, FuelType.AI95, FuelType.AI98, FuelType.DT],
            4: [FuelType.AI92, FuelType.AI95, FuelType.DT],
            5: [FuelType.AI92, FuelType.AI95, FuelType.DT],
            6: [FuelType.AI92, FuelType.AI95, FuelType.AI98, FuelType.DT],
            7: [FuelType.AI95, FuelType.DT],
            8: [FuelType.AI95, FuelType.DT]
        }

        # Назначаем цистерн
        for pump_id, fuels in pump_config.items():
            nozzles = []
            for fuel in fuels:
                if fuel == FuelType.AI95:
                    # Колонки 1-4 -> цистерна 1, 5-8 -> цистерна 2
                    tank_id = 1 if pump_id <= 4 else 2
                else:
                    tank_id = 1
                tank = tank_map[(fuel, tank_id)]
                nozzles.append(Nozzle(fuel, tank))
            self.pumps.append(Pump(pump_id, nozzles))

    def save_to_files(self):
        data = {
            "tanks": [t.to_dict() for t in self.tanks],
            "operations": [op.to_dict() for op in self.operations],
            "stats": self.stats,
            "emergency_mode": self.emergency_mode
        }
        with open("gas_station_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_files(self):
        if not os.path.exists("gas_station_data.json"):
            return
        try:
            with open("gas_station_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.tanks = [Tank.from_dict(t) for t in data["tanks"]]
            self.operations = [Operation.from_dict(op) for op in data["operations"]]
            self.stats = data["stats"]
            self.emergency_mode = data.get("emergency_mode", False)

            # Пересоздается колонка с новыми ссылками на цистерны
            tank_map = {(t.fuel_type, t.tank_id): t for t in self.tanks}
            pump_config = {
                1: [FuelType.AI92, FuelType.AI95],
                2: [FuelType.AI92, FuelType.AI95],
                3: [FuelType.AI92, FuelType.AI95, FuelType.AI98, FuelType.DT],
                4: [FuelType.AI92, FuelType.AI95, FuelType.DT],
                5: [FuelType.AI92, FuelType.AI95, FuelType.DT],
                6: [FuelType.AI92, FuelType.AI95, FuelType.AI98, FuelType.DT],
                7: [FuelType.AI95, FuelType.DT],
                8: [FuelType.AI95, FuelType.DT]
            }
            self.pumps = []
            for pump_id, fuels in pump_config.items():
                nozzles = []
                for fuel in fuels:
                    if fuel == FuelType.AI95:
                        tank_id = 1 if pump_id <= 4 else 2
                    else:
                        tank_id = 1
                    tank = tank_map[(fuel, tank_id)]
                    nozzles.append(Nozzle(fuel, tank))
                self.pumps.append(Pump(pump_id, nozzles))
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")

    def log_operation(self, op_type: str, details: str):
        op = Operation(op_type, details)
        self.operations.append(op)
        if len(self.operations) > 100:  # лимит истории 100 записей
            self.operations.pop(0)

    def get_disabled_tanks(self) -> List[Tank]:
        return [t for t in self.tanks if not t.enabled]

    def serve_customer(self):
        if self.emergency_mode:
            print("АЗС заблокирована из-за аварийной ситуации!")
            input("Нажмите Enter для возврата в меню...")
            return

        print("\n--- Обслуживание клиента ---\n")
        print("Доступные колонки:")
        available_pumps = [p for p in self.pumps if p.get_available_fuels()]
        if not available_pumps:
            print("Нет доступных колонок!")
            input("Нажмите Enter для возврата в меню...")
            return

        for p in available_pumps:
            print(f"{p.pump_id}) Колонка {p.pump_id}")
        try:
            pump_id = int(input("\nВыберите колонку:\n> "))
            pump = next((p for p in self.pumps if p.pump_id == pump_id), None)
            if not pump:
                print("Неверный номер колонки.")
                input("Нажмите Enter для возврата в меню...")
                return

            available_fuels = pump.get_available_fuels()
            if not available_fuels:
                print("На этой колонке нет доступного топлива.")
                input("Нажмите Enter для возврата в меню...")
                return

            print(f"\nКолонка {pump_id}\n")
            print("Доступные виды топлива:")
            for i, nozzle in enumerate(available_fuels, 1):
                print(f"{i}) {nozzle.fuel_type} (цистерна {nozzle.get_tank_info()})")

            choice = int(input("\nВыберите тип топлива:\n> ")) - 1
            if choice < 0 or choice >= len(available_fuels):
                print("Неверный выбор.")
                input("Нажмите Enter для возврата в меню...")
                return

            nozzle = available_fuels[choice]
            liters = float(input("\nВведите количество литров:\n> "))
            if liters <= 0:
                print("Некорректное количество.")
                input("Нажмите Enter для возврата в меню...")
                return

            price_per_liter = self.FUEL_PRICES[nozzle.fuel_type]
            total = liters * price_per_liter
            print(f"\nСтоимоsсть:\n{liters} л × {price_per_liter:.2f} ₽ = {total:.2f} ₽\n")

            confirm = input("Подтвердить оплату? (y/n)\n> ").strip().lower()
            if confirm != 'y':
                print("Операция отменена.")
                input("Нажмите Enter для возврата в меню...")
                return

            try:
                nozzle.tank.withdraw(int(liters))
                self.stats["cars_served"] += 1
                self.stats["fuel_sold"][nozzle.fuel_type] += int(liters)
                self.stats["fuel_income"][nozzle.fuel_type] += total
                self.stats["total_income"] += total
                self.log_operation("Продажа", f"{int(liters)} л {nozzle.fuel_type} на колонке {pump_id}, сумма: {total:.2f} ₽")
                print("\nОперация выполнена успешно.\nСпасибо за покупку!")
            except ValueError as e:
                print(f"\nОШИБКА:\n{e}")
        except (ValueError, IndexError):
            print("Некорректный ввод.")
        input("\nНажмите Enter для возврата в меню...")

    def check_tanks(self):
        print("\n--- Состояние цистерн ---\n")
        for i, tank in enumerate(self.tanks, 1):
            print(f"{i}) {tank}")
        input("\nНажмите Enter для возврата в меню...")

    def refill_tank(self):
        if self.emergency_mode:
            print("Нельзя пополнять топливо в аварийном режиме!")
            input("Нажмите Enter для возврата в меню...")
            return

        print("\n--- Оформить пополнение топлива ---\n")
        print("Доступные цистерны:")
        for i, tank in enumerate(self.tanks, 1):
            print(f"{i}) {tank.fuel_type} №{tank.tank_id} | {tank.current_volume} / {tank.max_volume} л")

        try:
            idx = int(input("\nВыберите цистерну:\n> ")) - 1
            if idx < 0 or idx >= len(self.tanks):
                raise ValueError
            tank = self.tanks[idx]
            liters = int(input("Укажите количество литров:\n> "))
            if liters <= 0:
                raise ValueError
            tank.refill(liters)
            self.log_operation("Пополнение", f"Цистерна {tank.fuel_type} №{tank.tank_id}, +{liters} л")
            print("Пополнение успешно выполнено.")
        except (ValueError, KeyError):
            print("Ошибка: некорректные данные.")
        except Exception as e:
            print(f"Ошибка: {e}")
        input("\nНажмите Enter для возврата в меню...")

    def show_balance(self):
        print("\n--- Баланс и статистика ---\n")
        print(f"Обслужено автомобилей: {self.stats['cars_served']}")
        print(f"Общий доход: {self.stats['total_income']:,.2f} ₽\n")
        print("Продано топлива:")
        for ft in [FuelType.AI92, FuelType.AI95, FuelType.AI98, FuelType.DT]:
            liters = self.stats["fuel_sold"][ft]
            income = self.stats["fuel_income"][ft]
            print(f"{ft:<6} - {liters} л ({income:,.2f} ₽)")
        input("\nНажмите Enter для возврата в меню...")

    def show_history(self):
        print("\n--- История операций ---\n")
        if not self.operations:
            print("История пуста.")
        else:
            for op in reversed(self.operations[-20:]):  # последние 20 операций
                print(op)
        input("\nНажмите Enter для возврата в меню...")

    def transfer_fuel(self):
        if self.emergency_mode:
            print("Нельзя перекачивать топливо в аварийном режиме!")
            input("Нажмите Enter для возврата в меню...")
            return

        print("\n--- Перекачка топлива между цистернами ---\n")
        print("Источник:")
        sources = [t for t in self.tanks if t.enabled]
        if not sources:
            print("Нет активных цистерн для перекачки.")
            input("Нажмите Enter для возврата в меню...")
            return

        for i, t in enumerate(sources, 1):
            print(f"{i}) {t.fuel_type} №{t.tank_id} | {t.current_volume} / {t.max_volume} л")
        try:
            src_idx = int(input("\nВыберите источник:\n> ")) - 1
            if src_idx < 0 or src_idx >= len(sources):
                raise ValueError
            source = sources[src_idx]

            print("\nПриемник (только тот же тип топлива):")
            targets = [t for t in self.tanks if t.fuel_type == source.fuel_type and t != source]
            if not targets:
                print("Нет подходящих цистерн для приема.")
                input("Нажмите Enter для возврата в меню...")
                return
            for i, t in enumerate(targets, 1):
                free = t.max_volume - t.current_volume
                print(f"{i}) {t.fuel_type} №{t.tank_id} | свободно: {free} л")
            tgt_idx = int(input("\nВыберите приемник:\n> ")) - 1
            if tgt_idx < 0 or tgt_idx >= len(targets):
                raise ValueError
            target = targets[tgt_idx]

            liters = int(input("Объем для перекачки (л):\n> "))
            if liters <= 0 or liters > source.current_volume:
                raise ValueError("Недостаточно топлива в источнике")
            if liters > (target.max_volume - target.current_volume):
                raise ValueError("Недостаточно места в приемнике")

            source.withdraw(liters)
            target.refill(liters)
            self.log_operation("Перекачка", f"{liters} л {source.fuel_type} из №{source.tank_id} в №{target.tank_id}")
            print("Перекачка успешно выполнена.")
        except Exception as e:
            print(f"Ошибка: {e}")
        input("\nНажмите Enter для возврата в меню...")

    def manage_tanks(self):
        if self.emergency_mode:
            print("Управление цистернами недоступно в аварийном режиме!")
            input("Нажмите Enter для возврата в меню...")
            return

        print("\n--- Управление цистернами ---\n")
        print("Доступные действия:")
        print("1) Включить цистерну")
        print("2) Отключить цистерну")
        try:
            action = input("> ").strip()
            if action == "1":
                disabled = [t for t in self.tanks if not t.enabled]
                if not disabled:
                    print("Нет отключенных цистерн.")
                else:
                    print("Цистерны, доступные для включения:")
                    for i, t in enumerate(disabled, 1):
                        print(f"{i}) {t.fuel_type} №{t.tank_id} | {t.current_volume} / {t.max_volume} л")
                    idx = int(input("\nВыберите цистерну:\n> ")) - 1
                    if 0 <= idx < len(disabled):
                        tank = disabled[idx]
                        if tank.current_volume >= tank.min_level:
                            tank.enabled = True
                            self.log_operation("Включение", f"Цистерна {tank.fuel_type} №{tank.tank_id}")
                            print(f"Цистерна {tank.fuel_type} №{tank.tank_id} успешно включена.")
                        else:
                            print("Уровень топлива ниже минимального! Включение невозможно.")
            elif action == "2":
                enabled = [t for t in self.tanks if t.enabled]
                if not enabled:
                    print("Нет включенных цистерн.")
                else:
                    print("Цистерны для отключения:")
                    for i, t in enumerate(enabled, 1):
                        print(f"{i}) {t}")
                    idx = int(input("\nВыберите цистерну:\n> ")) - 1
                    if 0 <= idx < len(enabled):
                        tank = enabled[idx]
                        tank.enabled = False
                        self.log_operation("Отключение", f"Цистерна {tank.fuel_type} №{tank.tank_id}")
                        print(f"Цистерна {tank.fuel_type} №{tank.tank_id} отключена.")
            else:
                print("Неверный выбор.")
        except Exception as e:
            print(f"Ошибка: {e}")
        input("\nНажмите Enter для возврата в меню...")

    def show_pumps(self):
        print("\n--- Состояние колонок ---\n")
        for pump in self.pumps:
            print(f"Колонка {pump.pump_id}:")
            for nozzle in pump.get_all_fuels():
                status = "РАБОТАЕТ" if nozzle.is_available() else "НЕ РАБОТАЕТ"
                print(f"  - {nozzle.fuel_type} (цистерна {nozzle.get_tank_info()}) → {status}")
        input("\nНажмите Enter для возврата в меню...")

    def emergency(self):
        if self.emergency_mode:
            print("\nАЗС уже в аварийном режиме!")
        else:
            self.emergency_mode = True
            for tank in self.tanks:
                tank.enabled = False
            self.log_operation("АВАРИЯ", "Система переведена в аварийный режим")
            print("\n!!! АВАРИЙНАЯ СИТУАЦИЯ !!!")
            print("Все цистерны заблокированы.")
            print("Имитируется вызов аварийных служб...")
        input("\nНажмите Enter для возврата в меню...")

    def exit_emergency(self):
        if not self.emergency_mode:
            print("АЗС не в аварийном режиме.")
        else:
            self.emergency_mode = False
            self.log_operation("Выход из аварии", "Аварийный режим отключен")
            print("Аварийный режим отключен. Цистерны остаются отключенными — включайте вручную.")
        input("\nНажмите Enter для возврата в меню...")

    def show_warning(self):
        disabled = self.get_disabled_tanks()
        if disabled:
            print("ВНИМАНИЕ!")
            print("Обнаружены отключённые цистерны:")
            for t in disabled:
                reason = "низкий уровень топлива" if t.is_low() else "вручную"
                print(f" - {t.fuel_type} №{t.tank_id} ({reason})")
            print()

    def run(self):
        self.load_from_files()
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("========================================")
            print("АЗС <<СеверНефть>>")
            print("Система управления заправочной станцией")
            print("========================================\n")

            if self.emergency_mode:                             #аварийный режиим
                print("!!! АВАРИЙНЫЙ РЕЖИМ АКТИВЕН !!!\n") 
            else:
                self.show_warning()

            print("Выберите действие:")
            print("1) Обслужить клиента (касса)")
            print("2) Проверить состояние цистерн")
            print("3) Оформить пополнение топлива")
            print("4) Баланс и статистика")
            print("5) История операций")
            print("6) Перекачка топлива между цистернами")
            print("7) Включение / отключение цистерн")
            print("8) Состояние колонок")
            if self.emergency_mode:
                print("E) Выйти из аварийного режима")
            else:
                print("9) EMERGENCY - аварийная ситуация")
            print("0) Выход")

            choice = input("> ").strip()

            if choice == "1":
                self.serve_customer()
            elif choice == "2":
                self.check_tanks()
            elif choice == "3":
                self.refill_tank()
            elif choice == "4":
                self.show_balance()
            elif choice == "5":
                self.show_history()
            elif choice == "6":
                self.transfer_fuel()
            elif choice == "7":
                self.manage_tanks()
            elif choice == "8":
                self.show_pumps()
            elif choice == "9" and not self.emergency_mode:
                self.emergency()
            elif choice.upper() == "E" and self.emergency_mode:
                self.exit_emergency()
            elif choice == "0":
                self.save_to_files()
                print("Данные сохранены. До свидания!")
                break
            else:
                print("Неверный выбор.")
                input("Нажмите Enter для продолжения...")


# Запуск программы

if __name__ == "__main__":
    station = GasStation()
    station.run()