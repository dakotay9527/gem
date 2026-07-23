# 相册拾光官网双平台下载导航设计

## 目标

修正官网首屏的下载行为和 iOS 状态：Android 首屏按钮跳转到现有二维码下载卡片，iOS 显示已经上线的 App Store v1.1 入口。

## 已确认的发布信息

- Android 官网版本：v1.0.0，Android 10–16，APK 38 MB。
- iOS App Store 版本：v1.1。
- App Store ID：`6788588179`。
- App Store 地址：`https://apps.apple.com/app/id6788588179`。
- iOS 最低系统版本：iOS 17.0。

## 交互设计

- 首屏橙色 Android 按钮从 APK 直链改为页面内锚点 `#android-download`。
- 按钮文案改为“扫码下载 / Android 版”，明确点击后会进入扫码区域。
- 现有二维码卡片增加 `id="android-download"`，并设置滚动定位间距。
- 二维码卡片中的“无法扫码？直接下载”保留为页面唯一带 `download` 属性的 APK 链接。
- 首屏 iOS 提示从“App Store 敬请期待”改成指向真实 App Store 页面、显示 v1.1 的可点击链接。

## 可访问性与响应式

- Android 首屏按钮使用说明跳转目标的 `aria-label`。
- 二维码卡片作为锚点目标，键盘与屏幕阅读器用户能理解跳转结果。
- iOS 链接明确包含设备、App Store 和版本信息。
- 现有桌面与移动布局结构不变，只增强链接状态与焦点样式。

## 测试

- 验证首屏 Android 按钮指向 `#android-download`，且不再直接下载 APK。
- 验证二维码卡片具有 `id="android-download"`。
- 验证页面仍只有一个带 `download` 属性的 APK 链接，且位于扫码卡片中。
- 验证 iOS App Store 地址、v1.1 和 iOS 17 信息存在。
- 保留二维码解码、APK 哈希和响应式样式测试。
