class DomainUtils:
    @staticmethod
    def copy(source, target):
        for attribute in target.__dict__:
            if hasattr(source, attribute):
                setattr(target, attribute, getattr(source, attribute))