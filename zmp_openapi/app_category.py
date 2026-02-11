"""
Mini App category constants.

This module contains predefined category names for Zalo Mini Apps.
These categories are used when creating a new Mini App.

Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/list-categories/
"""


class AppCategory:
    """
    Predefined Mini App category constants.

    These constants represent the available categories for Mini Apps.
    Use these values when creating a Mini App with the appCategory parameter.

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/list-categories/

    Example:
        >>> from zmp_openapi.app_category import AppCategory
        >>> from zmp_openapi.models import AppInfo
        >>> app_info = AppInfo(
        ...     appName="My App",
        ...     appDescription="Description",
        ...     appCategory=AppCategory.ECOMMERCE,
        ...     appSubCategory="fashion",
        ...     appLogoUrl="https://example.com/logo.png",
        ...     browsable=True
        ... )
    """
    BUSINESS = "Kinh doanh"
    ECOMMERCE = "Thương mại điện tử"
    EDUCATION = "Giáo dục"
    FINANCE = "Tài chính"
    GAME = "Trò chơi"
    GOVERNMENT = "Nhà nước & Chính phủ"
    HEALTH = "Sức khỏe"
    IMAGES = "Hình ảnh & Video"
    NEWS = "Thông tin & Báo chí"
    OFFLINE_SALE = "Bán hàng Offline"
    SOUND = "Âm thanh & Radio"
    TOOLS = "Công cụ phát triển"
    TRAVELING = "Du lịch"
    DEMO = "Thử nghiệm"
    UTILITIES = "Tiện ích"
    OTHERS = "Khác"
