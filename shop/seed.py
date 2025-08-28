from shop.models import Category, SubCategory, Product

def run():
    # Category
    cat1, _ = Category.objects.get_or_create(name='Electronics & Gadgets')
    cat2, _ = Category.objects.get_or_create(name='Cameras')

    # Subcategories
    laptops_sub, _ = SubCategory.objects.get_or_create(name='Laptops', parent=cat1)
    smartphones_sub, _ = SubCategory.objects.get_or_create(name='Smartphones', parent=cat1)
    digital_cam_sub, _ = SubCategory.objects.get_or_create(name='Digital Cameras', parent=cat2)

    # Laptops
    Product.objects.get_or_create(
        name='Asus Zenbook 14',
        price=524840,
        subcategory=laptops_sub,
        description='Устройство оснащено процессором Core i5-12500H с базовой частотой 1.2 GHz, что позволяет уверенно справляться с многозадачностью и запуском требовательных приложений.',
        image='uploads/products/product_image_105816_1306734.webp'
    )
    Product.objects.get_or_create(
        name='Dell XPS 13',
        price=751401,
        subcategory=laptops_sub,
        description='Ультрабук с процессором Intel Core i7 и дисплеем 4K.',
        image='uploads/products/product_image_93427_1256094.webp'
    )

    # Smartphones
    Product.objects.get_or_create(
        name='Samsung Galaxy A55',
        price=299999,
        subcategory=smartphones_sub,
        description='Смартфон с AMOLED дисплеем и батареей 5000 мАч.',
        image='uploads/products/cze6vo443eess4sel3u894loixvkr4uu'
    )
    Product.objects.get_or_create(
        name='iPhone 15',
        price=499999,
        subcategory=smartphones_sub,
        description='Новый iPhone с процессором A16 Bionic.',
        image='uploads/products/download.jpeg'
    )

    # Digital Cameras
    Product.objects.get_or_create(
        name='Kodak PixPro FZ55',
        price=165000,
        subcategory=digital_cam_sub,
        description='Компактная камера с 20 МП сенсором и 5x оптическим зумом.',
        image='uploads/products/download (1).jpeg'
    )