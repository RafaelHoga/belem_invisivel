from django import forms
from .models import Avaliacao


class AvaliacaoForm(forms.ModelForm):
    """
    Formulário para criação de avaliações.
    Valida que a nota está entre 1 e 5.
    """
    
    class Meta:
        model = Avaliacao
        fields = ['ponto_turistico', 'nota', 'comentario']
        widgets = {
            'ponto_turistico': forms.HiddenInput(),
            'comentario': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'nota': forms.Select(
                choices=[(i, f'{i} estrela{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            )
        }
    
    def clean_nota(self):
        """Valida que a nota está entre 1 e 5"""
        nota = self.cleaned_data.get('nota')
        if nota is None or nota < 1 or nota > 5:
            raise forms.ValidationError('A nota deve estar entre 1 e 5 estrelas.')
        return nota
    
    def clean(self):
        """Validação adicional do formulário"""
        cleaned_data = super().clean()
        ponto_turistico = cleaned_data.get('ponto_turistico')
        user = self.user  # Será setado na view
        
        # Verifica se o usuário já avaliou este ponto
        if Avaliacao.objects.filter(
            ponto_turistico=ponto_turistico,
            usuario=user
        ).exists():
            raise forms.ValidationError('Você já avaliou este ponto turístico.')
        
        return cleaned_data