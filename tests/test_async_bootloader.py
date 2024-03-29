from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

import pytest

from buti import ButiKeys, ButiStore
from buti.core import AsyncBootableComponent, AsyncBootloader

pytestmark = pytest.mark.anyio


class MockComponent1(AsyncMock):
    pass


class MockComponent2(AsyncMock):
    pass


class DemoKeys(ButiKeys):
    any_object_key: str = "any_object_key"


class TestAsyncBootableComponent(IsolatedAsyncioTestCase):
    async def test_boot(self):
        try:
            bootable_component = AsyncMock()
            await bootable_component.boot(ButiStore())
        except NotImplementedError:
            pytest.fail("NotImplementedError was raised")

    async def test_post_boot(self):
        pass


class TestAsyncBootloader(IsolatedAsyncioTestCase):
    def setUp(self):
        self.boot_loader = AsyncBootloader()

    def test_add_component(self):
        component = MockComponent1()
        self.boot_loader.add_component(component)
        self.assertTrue(self.boot_loader.has_component(component))

    def test_add_components(self):
        components = [MockComponent1(), MockComponent2()]
        self.boot_loader.add_components(components)
        self.assertTrue(self.boot_loader.has_component(components[0]))
        self.assertTrue(self.boot_loader.has_component(components[1]))

    async def test_boot(self):
        component = AsyncMock(spec=AsyncBootableComponent)
        component.boot = AsyncMock()
        self.boot_loader.add_component(component)
        await self.boot_loader.boot()
        component.boot.assert_called_once()

    async def test_boot_calls_boot_and_post_boot_on_components(self):
        buti_store = ButiStore()
        boot_loader = AsyncBootloader(buti_store)

        component1 = MockComponent1()
        component2 = MockComponent2()

        boot_loader.add_component(component1)
        boot_loader.add_component(component2)

        await boot_loader.boot()

        component1.boot.assert_called_once_with(buti_store)
        component2.boot.assert_called_once_with(buti_store)

        component1.post_boot.assert_called_once_with(buti_store)
