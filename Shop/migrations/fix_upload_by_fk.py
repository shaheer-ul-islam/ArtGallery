from django.db import migrations

def fix_upload_by_fk(apps, schema_editor):
    Art = apps.get_model('Shop', 'Art')
    Seller = apps.get_model('Shop', 'Seller')
    
    for art in Art.objects.all():
        try:
            seller = Seller.objects.get(id=art.upload_by_id)
            # If this passes, the relationship is valid, no need to update
        except Seller.DoesNotExist:
            # Handle cases where no corresponding Seller exists if needed
            art.upload_by = None  # or any other appropriate action
            art.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0010_alter_art_upload_by'),  # replace with your actual last migration file name
    ]

    operations = [
        migrations.RunPython(fix_upload_by_fk),
    ]
