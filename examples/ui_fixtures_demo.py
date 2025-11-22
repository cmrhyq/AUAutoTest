"""
UI Fixtures 使用示例

演示如何使用 UI 测试 fixtures 进行测试。
"""

import pytest
from base.ui.pages.base_page import BasePage


def test_basic_navigation(page):
    """
    演示基本的页面导航功能
    
    使用 page fixture 自动管理浏览器页面的生命周期。
    """
    # 创建页面对象
    base_page = BasePage(page)
    
    # 导航到示例网站
    base_page.navigate("https://example.com")
    
    # 验证页面标题
    title = base_page.get_title()
    assert "Example Domain" in title
    
    # 获取页面 URL
    url = base_page.get_current_url()
    assert "example.com" in url


def test_element_interaction(page):
    """
    演示元素交互功能
    
    展示如何使用智能等待和元素操作。
    """
    base_page = BasePage(page)
    
    # 导航到示例网站
    base_page.navigate("https://example.com")
    
    # 等待并获取元素文本
    # 注意：example.com 是一个简单的页面，这里只是演示用法
    if base_page.is_visible("h1"):
        heading_text = base_page.get_text("h1")
        print(f"页面标题: {heading_text}")


def test_screenshot_capture(page):
    """
    演示截图功能
    
    展示如何手动截图和自动截图（失败时）。
    """
    base_page = BasePage(page)
    
    # 导航到示例网站
    base_page.navigate("https://example.com")
    
    # 手动截图
    screenshot = base_page.take_screenshot("example_page")
    assert screenshot is not None
    assert len(screenshot) > 0


@pytest.mark.skip(reason="演示失败时自动截图功能")
def test_auto_screenshot_on_failure(page):
    """
    演示失败时自动截图功能
    
    当测试失败时，auto_screenshot_on_failure fixture 会自动捕获截图。
    """
    base_page = BasePage(page)
    
    # 导航到示例网站
    base_page.navigate("https://example.com")
    
    # 故意让测试失败以触发自动截图
    assert False, "这是一个故意失败的测试，用于演示自动截图功能"


def test_browser_context_isolation(page):
    """
    演示浏览器上下文隔离
    
    每个测试都有独立的浏览器上下文，确保测试之间不会相互影响。
    """
    base_page = BasePage(page)
    
    # 导航到示例网站
    base_page.navigate("https://example.com")
    
    # 执行一些操作
    # 这些操作不会影响其他测试
    current_url = base_page.get_current_url()
    assert "example.com" in current_url


if __name__ == "__main__":
    # 运行示例测试
    # pytest examples/ui_fixtures_demo.py -v
    print("请使用 pytest 运行此文件:")
    print("pytest examples/ui_fixtures_demo.py -v")
