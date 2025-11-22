"""
BasePage 使用示例

演示如何使用 BasePage 类创建页面对象和执行常见操作。
"""

from playwright.sync_api import sync_playwright
from base.ui.pages.base_page import BasePage
from core.log.logger import TestLogger


def demo_base_page():
    """演示 BasePage 的基本用法"""
    
    # 初始化日志
    TestLogger.setup_logger()
    logger = TestLogger.get_logger("BasePage Demo")
    
    logger.info("Starting BasePage demo")
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 创建 BasePage 实例
        base_page = BasePage(page)
        
        try:
            # 1. 导航到页面
            logger.info("Demo 1: Navigate to page")
            base_page.navigate("https://example.com")
            
            # 2. 获取页面信息
            logger.info("Demo 2: Get page information")
            title = base_page.get_title()
            url = base_page.get_current_url()
            logger.info(f"Page title: {title}")
            logger.info(f"Current URL: {url}")
            
            # 3. 等待元素
            logger.info("Demo 3: Wait for element")
            h1_element = base_page.wait_for_element("h1")
            
            # 4. 获取文本
            logger.info("Demo 4: Get text from element")
            h1_text = base_page.get_text("h1")
            logger.info(f"H1 text: {h1_text}")
            
            # 5. 检查元素可见性
            logger.info("Demo 5: Check element visibility")
            is_visible = base_page.is_visible("h1")
            logger.info(f"H1 is visible: {is_visible}")
            
            # 6. 截图
            logger.info("Demo 6: Take screenshot")
            base_page.take_screenshot("example_page", attach_to_allure=False)
            
            # 7. 执行 JavaScript
            logger.info("Demo 7: Execute JavaScript")
            page_height = base_page.execute_script("return document.body.scrollHeight")
            logger.info(f"Page height: {page_height}px")
            
            logger.info("BasePage demo completed successfully")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            base_page.take_screenshot("demo_error", attach_to_allure=False)
            raise
        finally:
            browser.close()


def demo_page_object_pattern():
    """演示如何使用 Page Object 模式创建具体页面类"""
    
    class ExamplePage(BasePage):
        """Example.com 页面对象"""
        
        # 定义页面元素选择器
        HEADING = "h1"
        PARAGRAPH = "p"
        MORE_INFO_LINK = "a"
        
        def __init__(self, page):
            super().__init__(page)
            self.url = "https://example.com"
        
        def open(self):
            """打开页面"""
            self.navigate(self.url)
        
        def get_heading_text(self):
            """获取标题文本"""
            return self.get_text(self.HEADING)
        
        def get_paragraph_text(self):
            """获取段落文本"""
            return self.get_text(self.PARAGRAPH)
        
        def click_more_info(self):
            """点击 More information 链接"""
            self.click(self.MORE_INFO_LINK)
    
    # 使用页面对象
    TestLogger.setup_logger()
    logger = TestLogger.get_logger("Page Object Demo")
    
    logger.info("Starting Page Object pattern demo")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # 创建页面对象实例
            example_page = ExamplePage(page)
            
            # 使用页面对象方法
            example_page.open()
            
            heading = example_page.get_heading_text()
            paragraph = example_page.get_paragraph_text()
            
            logger.info(f"Heading: {heading}")
            logger.info(f"Paragraph: {paragraph}")
            
            # 截图
            example_page.take_screenshot("page_object_demo", attach_to_allure=False)
            
            logger.info("Page Object pattern demo completed successfully")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    print("=" * 60)
    print("BasePage Demo")
    print("=" * 60)
    
    # 运行基础演示
    demo_base_page()
    
    print("\n" + "=" * 60)
    print("Page Object Pattern Demo")
    print("=" * 60)
    
    # 运行 Page Object 模式演示
    demo_page_object_pattern()
