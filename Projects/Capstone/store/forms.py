from django import forms

class QuizForm(forms.Form):
    rather_be = forms.ChoiceField(choices=(('A', 'Private Beach/Garden'), ('B', 'Ski Resort/Hiking')),label ="rather_be")
    drink = forms.ChoiceField(choices=(('A', 'Manhattan'), ('B', 'Cosmopolitan')),label ="drink")
    wardrobe = forms.ChoiceField(choices=(('A', 'Bright color clothing(red, pink, orange)'), ('B', 'Dark color clothing(black, brown, gray,etc')),label ="wardrobe")
    friendship_group = forms.ChoiceField(choices=(('A', 'The shoulder to cry on'), ('B', 'The party planner')),label ="friendship_group")
    most_happy = forms.ChoiceField(choices=(('A', 'Enjoying sunshine and outdoor festivals'), ('B', 'Enjoying pumpkin spice and fall activities')),label ="most_happy")



    def clean(self):
        cleaned_data = super().clean()