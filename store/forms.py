from django import forms
from .models import ReviewRating, Product


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']



# def clean(self):
    #     cd = super(ReviewForm, self).clean()

    #     rating =cd.get('rating')
    #     if rating =''  :
    #        raise forms.ValidationError('لطفا بخش امتیاز دهی (⭐) را تکمیل نمایید. با تشکر')
