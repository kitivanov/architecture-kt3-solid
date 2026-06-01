"""
В модуле реализована демонстрационная система уведомлений,
реализованная по принципам SOLID.

SOLID - это принципы разработки программного обеспечения, следуя которым Вы получите хороший код,
который в дальнейшем будет хорошо масштабироваться и поддерживаться в рабочем состоянии.

S - Single Responsibility Principle - принцип единственной ответственности.
  Каждый класс должен иметь только одну зону ответственности.
O - Open closed Principle - принцип открытости-закрытости.
  Классы должны быть открыты для расширения, но закрыты для изменения.
L - Liskov substitution Principle - принцип подстановки Барбары Лисков.
  Должна быть возможность вместо базового (родительского) типа (класса) подставить любой его подтип (класс-наследник),
  при этом работа программы не должна измениться.
I -  Interface Segregation Principle - принцип разделения интерфейсов.
  Данный принцип обозначает, что не нужно заставлять клиента (класс) реализовывать интерфейс,
  который не имеет к нему отношения.
D - Dependency Inversion Principle - принцип инверсии зависимостей.
  Модули верхнего уровня не должны зависеть от модулей нижнего уровня.
  И те, и другие должны зависеть от абстракции.
  Абстракции не должны зависеть от деталей. Детали должны зависеть от абстракций.
"""
from abc import ABC, abstractmethod


class NotificationSender(ABC):
    """
    Абстрактный интерфейс отправки уведомлений.

    Принцип D (Dependency Inversion): высокоуровневые модули работают через абстракцию.
    """

    @abstractmethod
    def send(self, msg: str):
        """
        Отправить сообщение.
        """
        pass


class EmailSender(NotificationSender):
    """
    Реализация отправки уведомлений по электронной почте.

    Принципы:
        O — можно добавлять новые способы отправки
            без изменения существующего кода.
        L — может использоваться вместо NotificationSender.
    """
    def send(self, msg: str):
        print(f"[EMAIL] Отправлено: {msg}")


class SmsSender(NotificationSender):
    """
    Реализация отправки уведомлений через смс.

    Принципы:
        O — можно добавлять новые способы отправки
            без изменения существующего кода.
        L — может использоваться вместо NotificationSender.
    """
    def send(self, msg: str):
        print(f"[SMS] Отправлено: {msg}")


class TelegramSender(NotificationSender):
    """
    Реализация отправки уведомлений через Telegram.

    Принципы:
        O — можно добавлять новые способы отправки
            без изменения существующего кода.
        L — может использоваться вместо NotificationSender.
    """
    def send(self, msg: str):
        print(f"[TELEGRAM] Отправлено: {msg}")


class MessageFormatter:
    """
    Отвечает только за форматирование текста.

    Принцип S (Single Responsibility): изменение формата сообщений не влияет
      на логику отправки.
    """
    def format(self, text: str) -> str:
        """
        Подготавливает текст уведомления.
        """
        return f"Уведомление: {text}"


class Logger:
    """
    Выполняет только логирование событий.

    Принцип I (Interface Segregation): логирование вынесено отдельно.
    """
    def log(self, text: str):
        """
        Записать сообщение в журнал.
        """
        print(f"[LOG] {text}")


class NotificationService:
    """
    Основной сервис отправки уведомлений.
    Использует абстракцию отправителя, форматирование и логирование.

    Принципы:
        S — координация процесса отправки.
        D — зависимости передаются извне.
    """
    def __init__(
        self,
        sender: NotificationSender,
        formatter: MessageFormatter,
        logger: Logger
    ):
        self.sender = sender
        self.formatter = formatter
        self.logger = logger

    def notify(self, text: str):
        """
        Выполнить отправку уведомления.
        """
        msg = self.formatter.format(text)

        self.sender.send(msg)

        self.logger.log(
            f"Сообщение отправлено через "
            f"{self.sender.__class__.__name__}"
        )


def main():
    formatter = MessageFormatter()
    logger = Logger()

    email_service = NotificationService(EmailSender(), formatter, logger)
    sms_service = NotificationService(SmsSender(), formatter, logger)
    telegram_service = NotificationService(TelegramSender(), formatter, logger)

    email_service.notify("Заказ оформлен.")
    sms_service.notify("Ваш код подтверждения - 1234. Никому не сообщайте его.")
    telegram_service.notify("Уведомляем вас о новых поступлениях!")


if __name__ == "__main__":
    main()
