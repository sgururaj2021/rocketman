from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


class HomePage(Page):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["flex.FlexPage", "services.ServiceListingPage", "contact.ContactPage"]
    max_count = 1
    lead_text = models.CharField(
        max_length=140,
        blank=True,
        help_text='Subheading text under the banner title',
    )

    button = models.ForeignKey(
        'wagtailcore.Page',
        blank= True,
        null= True,
        related_name= '+',
        help_text= 'Select an optional page to link to',
        on_delete= models.SET_NULL,
    )

    button_text = models.CharField(
        max_length=50,
        default= 'Read More',
        blank= False,
        help_text= 'Button text',
    )

    banner_background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank= False,
        null= True,
        related_name= '+',
        help_text= 'The banner background image',
        on_delete= models.SET_NULL,
    )

    body = StreamField([
        ("title", blocks.TitleBlock()),
        ("cards", blocks.CardsBlock()),
        ("image_and_text", blocks.ImageAndTextBlock()),
        ("card_to_action", blocks.CallToActionBlock()),
        ("testimonial", blocks.SnippetChooserBlock(
            target_model = 'testimonials.Testimonial',
            template = "streams/testimonial_block.html",
        )),
        ("pricing_table", blocks.PricingTableBlock()),
    ], null = True, blank = True)


    content_panels = Page.content_panels + [
        FieldPanel("lead_text"),
        PageChooserPanel("button"),
        FieldPanel("button_text"),
        ImageChooserPanel("banner_background_image"),
        StreamFieldPanel("body"),
    ]

    def save(self, *args, **kwargs):
        key = make_template_fragment_key(
            "home_page_streams",
            [self.id],
        )

        cache.delete(key)
        return super().save(*args, **kwargs)