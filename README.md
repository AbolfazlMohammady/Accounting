<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پروژه حسابداری آنلاین</title>
    <style>
        body {
            font-family: 'Vazir', Arial, sans-serif;
            line-height: 1.8;
            direction: rtl;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #0073e6;
        }
        ul {
            margin: 0;
            padding-left: 20px;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 4px;
            font-family: monospace;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: #fff;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .code-block {
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            white-space: pre;
            overflow-x: auto;
            border-left: 5px solid #0073e6;
            margin-bottom: 20px;
        }
        .section-title {
            border-bottom: 2px solid #0073e6;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        hr {
            border: 0;
            height: 1px;
            background: #ccc;
            margin: 30px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>پروژه حسابداری آنلاین با Django</h1>

        <section>
            <h2 class="section-title">معرفی پروژه</h2>
            <p>
                این پروژه یک سیستم حسابداری آنلاین است که با استفاده از فریم‌ورک قدرتمند <strong>Django</strong> طراحی و پیاده‌سازی شده است. هدف این سیستم مدیریت کاربران، پروفایل‌ها، نقش‌ها، و ارائه ابزارهای حسابداری برای کاربران با سطوح دسترسی مختلف (کاربر عادی، ادمین، مدیر مالی) می‌باشد.
            </p>
        </section>

        <hr>

        <section>
            <h2 class="section-title">ویژگی‌ها و امکانات</h2>

            <h3>مدیریت کاربران</h3>
            <ul>
                <li><strong>سیستم احراز هویت سفارشی:</strong> ثبت‌نام، ورود و مدیریت کاربران با شماره تلفن یا ایمیل.</li>
                <li><strong>پشتیبانی از نقش‌ها:</strong> تعریف و مدیریت نقش‌های مختلف (کاربر عادی، ادمین، مدیر مالی).</li>
                <li><strong>پروفایل کاربری:</strong> هر کاربر می‌تواند پروفایل خود را شامل تصویر، اطلاعات شخصی، و بیوگرافی مدیریت کند.</li>
            </ul>

            <h3>سطوح دسترسی</h3>
            <ul>
                <li>نقش‌ها به کاربران اختصاص داده می‌شود تا دسترسی به بخش‌های مختلف سیستم کنترل شود.</li>
                <li>هر کاربر می‌تواند چندین نقش داشته باشد (مانند ادمین و مدیر مالی).</li>
            </ul>

            <h3>ولیدیشن و امنیت</h3>
            <ul>
                <li><strong>اعتبارسنجی شماره تلفن:</strong> فقط شماره‌های معتبر ایران پذیرفته می‌شوند.</li>
                <li><strong>امنیت بالا:</strong> استفاده از استانداردهای Django برای مدیریت کلمات عبور و داده‌های حساس.</li>
            </ul>

            <h3>ساختار ماژولار</h3>
            <ul>
                <li>طراحی شده به صورت ماژولار برای سهولت توسعه و گسترش در آینده.</li>
                <li>قابلیت افزودن ویژگی‌های جدید مانند گزارش‌گیری، مدیریت پرداخت‌ها، و صورتحساب.</li>
            </ul>
        </section>

        <hr>

        <section>
            <h2 class="section-title">فناوری‌های استفاده شده</h2>
            <ul>
                <li><strong>Backend:</strong> Django 4.x</li>
                <li><strong>پایگاه داده:</strong> PostgreSQL (یا هر دیتابیس دلخواه دیگر)</li>
                <li><strong>احراز هویت:</strong> استفاده از سیستم AbstractUser برای سفارشی‌سازی کامل.</li>
                <li><strong>مدیریت فایل‌های مدیا:</strong> استفاده از سیستم <code>ImageField</code> برای بارگذاری تصاویر پروفایل.</li>
            </ul>
        </section>

        <hr>

        <section>
            <h2 class="section-title">ساختار پروژه</h2>
            <div class="code-block">
accounts/ │ ├── migrations/ # فایل‌های مهاجرت دیتابیس ├── models.py # مدل‌های کاربری و پروفایل ├── serializers.py # سریالایزرهای API برای مدیریت کاربران و نقش‌ها ├── views.py # ویوها برای ثبت‌نام، ورود، و مدیریت پروفایل ├── urls.py # مسیرهای مرتبط با کاربران ├── validators.py # اعتبارسنجی داده‌ها (مانند شماره تلفن) └── tests.py # تست‌های واحد برای تضمین صحت عملکرد
            </div>
        </section>
    </div>
</body>
</html>
