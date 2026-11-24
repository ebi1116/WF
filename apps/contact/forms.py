from django import forms

from .models import ContactEnquiry, QuoteEnquiry


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")


class ContactEnquiryForm(StyledFormMixin, forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off", "aria-hidden": "true"}))

    class Meta:
        model = ContactEnquiry
        fields = ("full_name", "email", "phone", "service", "subject", "message")
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}

    def clean_website(self):
        if self.cleaned_data["website"]:
            raise forms.ValidationError("Unable to submit this form.")
        return ""


class QuoteEnquiryForm(StyledFormMixin, forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off", "aria-hidden": "true"}))

    class Meta:
        model = QuoteEnquiry
        fields = ("customer_name", "email", "phone", "company_name", "service", "budget", "timeline", "requirements")
        widgets = {"requirements": forms.Textarea(attrs={"rows": 5})}

    def clean_website(self):
        if self.cleaned_data["website"]:
            raise forms.ValidationError("Unable to submit this form.")
        return ""
