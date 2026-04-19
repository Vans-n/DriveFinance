from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.db.models import Sum
from .models import Corrida, Despesa, Motorista
from .forms import CorridaForm
from .forms import DespesaForm


#DASHBOARD
@login_required
def dashboard(request):
    motorista = Motorista.objects.filter(usuario=request.user).first()

    if not motorista:
        return render(request, 'dashboard.html', {
            'erro': 'Motorista não encontrado.'
        })

    # Totais gerais
    total_corridas = Corrida.objects.filter(motorista=motorista).aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = Despesa.objects.filter(motorista=motorista).aggregate(Sum('valor'))['valor__sum'] or 0

    lucro = total_corridas - total_despesas

    # Totais por plataforma
    ganhos_por_plataforma = (
        Corrida.objects
        .filter(motorista=motorista)
        .values('plataforma__nome')
        .annotate(total=Sum('valor'))
    ) or []

    context = {
        'total_corridas': total_corridas,
        'total_despesas': total_despesas,
        'lucro': lucro,
        'ganhos_por_plataforma': ganhos_por_plataforma
    }

    return render(request, 'dashboard.html', context)


#LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuário ou senha inválidos")

    return render(request, 'login.html')


#LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


#CRIAR CORRIDA
@login_required
def criar_corrida(request):
    motorista = Motorista.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        post = request.POST.copy()
        valor = post.get('valor')

        # 🔥 Corrige vírgula para ponto
        if valor:
            post['valor'] = valor.replace(',', '.')

        form = CorridaForm(post)

        if form.is_valid():
            corrida = form.save(commit=False)
            corrida.motorista = motorista
            corrida.save()
            messages.success(request, "Corrida cadastrada com sucesso!")
            return redirect('listar_corridas')
    else:
        form = CorridaForm()

    return render(request, 'corridas/form.html', {'form': form})


#LISTAR CORRIDAS
@login_required
def listar_corridas(request):
    motorista = Motorista.objects.filter(usuario=request.user).first()
    corridas = Corrida.objects.filter(motorista=motorista)

    return render(request, 'corridas/listar.html', {'corridas': corridas})


#EDITAR CORRIDA
@login_required
def editar_corrida(request, id):
    motorista = Motorista.objects.filter(usuario=request.user).first()
    corrida = Corrida.objects.filter(id=id, motorista=motorista).first()

    if not corrida:
        messages.error(request, "Corrida não encontrada.")
        return redirect('listar_corridas')

    if request.method == 'POST':
        post = request.POST.copy()
        valor = post.get('valor')

        if valor:
            post['valor'] = valor.replace(',', '.')

        form = CorridaForm(post, instance=corrida)

        if form.is_valid():
            form.save()
            messages.success(request, "Corrida atualizada!")
            return redirect('listar_corridas')
    else:
        form = CorridaForm(instance=corrida)

    return render(request, 'corridas/form.html', {'form': form})


#EXCLUIR CORRIDA
@login_required
def excluir_corrida(request, id):
    motorista = Motorista.objects.filter(usuario=request.user).first()
    corrida = Corrida.objects.filter(id=id, motorista=motorista).first()

    if not corrida:
        messages.error(request, "Corrida não encontrada.")
        return redirect('listar_corridas')

    corrida.delete()
    messages.success(request, "Corrida excluída com sucesso!")
    return redirect('listar_corridas')

@login_required
def criar_despesa(request):
    motorista = Motorista.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        post = request.POST.copy()
        valor = post.get('valor')

        if valor:
            post['valor'] = valor.replace(',', '.')

        form = DespesaForm(post)

        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.motorista = motorista
            despesa.save()
            messages.success(request, "Despesa cadastrada!")
            return redirect('listar_despesas')
    else:
        form = DespesaForm()

    return render(request, 'despesas/form.html', {'form': form})

@login_required
def listar_despesas(request):
    motorista = Motorista.objects.filter(usuario=request.user).first()
    despesas = Despesa.objects.filter(motorista=motorista)

    return render(request, 'despesas/listar.html', {'despesas': despesas})

@login_required
def editar_despesa(request, id):
    motorista = Motorista.objects.filter(usuario=request.user).first()
    despesa = Despesa.objects.filter(id=id, motorista=motorista).first()

    if not despesa:
        return redirect('listar_despesas')

    if request.method == 'POST':
        post = request.POST.copy()
        valor = post.get('valor')

        if valor:
            post['valor'] = valor.replace(',', '.')

        form = DespesaForm(post, instance=despesa)

        if form.is_valid():
            form.save()
            return redirect('listar_despesas')
    else:
        form = DespesaForm(instance=despesa)

    return render(request, 'despesas/form.html', {'form': form})

@login_required
def excluir_despesa(request, id):
    if request.method == 'POST':
        motorista = Motorista.objects.filter(usuario=request.user).first()
        despesa = Despesa.objects.filter(id=id, motorista=motorista).first()

        if despesa:
            despesa.delete()
            messages.success(request, "Despesa excluída com sucesso!")

    return redirect('listar_despesas')

# CRIAR DESPESA
@login_required
def criar_despesa(request):
    motorista = Motorista.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        post = request.POST.copy()
        valor = post.get('valor')

        if valor:
            post['valor'] = valor.replace(',', '.')

        form = DespesaForm(post)

        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.motorista = motorista
            despesa.save()
            messages.success(request, "Despesa cadastrada com sucesso!")
            return redirect('listar_despesas')
    else:
        form = DespesaForm()

    return render(request, 'despesas/form.html', {'form': form})


# LISTAR DESPESAS
@login_required
def listar_despesas(request):
    motorista = Motorista.objects.filter(usuario=request.user).first()
    despesas = Despesa.objects.filter(motorista=motorista)

    return render(request, 'despesas/listar.html', {'despesas': despesas})


# EDITAR DESPESA
@login_required
def editar_despesa(request, id):
    motorista = Motorista.objects.filter(usuario=request.user).first()
    despesa = Despesa.objects.filter(id=id, motorista=motorista).first()

    if not despesa:
        messages.error(request, "Despesa não encontrada.")
        return redirect('listar_despesas')

    if request.method == 'POST':
        post = request.POST.copy()
        valor = post.get('valor')

        if valor:
            post['valor'] = valor.replace(',', '.')

        form = DespesaForm(post, instance=despesa)

        if form.is_valid():
            form.save()
            messages.success(request, "Despesa atualizada!")
            return redirect('listar_despesas')
    else:
        form = DespesaForm(instance=despesa)

    return render(request, 'despesas/form.html', {'form': form})


# EXCLUIR DESPESA
@login_required
def excluir_despesa(request, id):
    motorista = Motorista.objects.filter(usuario=request.user).first()
    despesa = Despesa.objects.filter(id=id, motorista=motorista).first()

    if not despesa:
        messages.error(request, "Despesa não encontrada.")
        return redirect('listar_despesas')

    despesa.delete()
    messages.success(request, "Despesa excluída com sucesso!")
    return redirect('listar_despesas')

from datetime import datetime

@login_required
def dashboard(request):
    motorista = Motorista.objects.filter(usuario=request.user).first()

    if not motorista:
        return render(request, 'dashboard.html', {'erro': 'Motorista não encontrado.'})

    hoje = datetime.now()

    # 🔥 FILTRO POR MÊS
    corridas = Corrida.objects.filter(
        motorista=motorista,
        data__month=hoje.month,
        data__year=hoje.year
    )

    despesas = Despesa.objects.filter(
        motorista=motorista,
        data__month=hoje.month,
        data__year=hoje.year
    )

    total_corridas = corridas.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas.aggregate(Sum('valor'))['valor__sum'] or 0

    lucro = total_corridas - total_despesas

    ganhos_por_plataforma = (
        corridas
        .values('plataforma__nome')
        .annotate(total=Sum('valor'))
    )

    context = {
        'total_corridas': total_corridas,
        'total_despesas': total_despesas,
        'lucro': lucro,
        'ganhos_por_plataforma': ganhos_por_plataforma
    }

    return render(request, 'dashboard.html', context)