from Domain.Commons.CoreServices import CoreServices as Services
from Domain.Interfaces.IFakeApiInfrastructure import IFakeApiInfrastructure
from Infrastructure.ExampleFakeApiInfra.Queries.FakeApiCommand import FakeApiCommand

class ExampleFakeApiSetting():
    @classmethod
    def add_services(self) ->None:
        Services.add_singleton_dependency(IFakeApiInfrastructure, FakeApiCommand)