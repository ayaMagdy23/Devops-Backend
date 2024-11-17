from django.db import models
class Script(models.Model):
    # Name or title of the script
    title = models.CharField(max_length=255)
    
    # Description or content of the script
    description = models.TextField()
    
    # Link or reference to the script file (optional)
    script_link = models.URLField(max_length=200, blank=True, null=True)
    
    # Date when the script was created or published
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: Category or tag to classify scripts
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
    
    from django.db import models

class Tool(models.Model):
    name = models.CharField(max_length=100)  # Name of the tool
    description = models.TextField()         # Description of the tool
    url = models.URLField(blank=True, null=True)  # URL (optional)

    def __str__(self):
        return self.name  # Just return the name as a string, not a tuple

