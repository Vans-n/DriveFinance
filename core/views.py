from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Sum
from .models import Corrida, Despesa, Motorista
from .forms import CorridaForm, DespesaForm
import json
from django.contrib.auth.models import User
from django.shortcuts import render


def get_motorista(user):
    return Motorista.objects.filter(usuario=user).first()


# DASHBOARD
@login_required
def dashboard(request):
    motorista = get_motorista(request.user)

    if not motorista:
        return render(request, 'dashboard.html', {'erro': 'Motorista não encontrado.'})

    hoje = datetime.now()
    periodo = request.GET.get('periodo')
    data_filtro = request.GET.get('data')

    corridas = Corrida.objects.filter(motorista=motorista)
    despesas = Despesa.objects.filter(motorista=motorista)

    if data_filtro:
        try:
            data_convertida = datetime.strptime(data_filtro, "%Y-%m-%d").date()
            corridas = corridas.filter(data=data_convertida)
            despesas = despesas.filter(data=data_convertida)
        except ValueError:
            return render(request, 'dashboard.html', {'erro': 'Data inválida.'})

    elif periodo == 'hoje':
        corridas = corridas.filter(data=hoje.date())
        despesas = despesas.filter(data=hoje.date())

    elif periodo == 'semana':
        sete_dias = hoje.date() - timedelta(days=7)
        corridas = corridas.filter(data__gte=sete_dias)
        despesas = despesas.filter(data__gte=sete_dias)

    elif periodo == 'mes':
        corridas = corridas.filter(data__month=hoje.month, data__year=hoje.year)
        despesas = despesas.filter(data__month=hoje.month, data__year=hoje.year)

    total_corridas = corridas.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas.aggregate(Sum('valor'))['valor__sum'] or 0
    lucro = total_corridas - total_despesas

    ganhos_por_plataforma = corridas.values('plataforma__nome').annotate(total=Sum('valor'))
    labels = [item['plataforma__nome'] for item in ganhos_por_plataforma]
    valores = [float(item['total']) for item in ganhos_por_plataforma]

    atividades = []

    for c in corridas:
        atividades.append({
            'data': c.data,
            'descricao': c.plataforma.nome,
            'valor': c.valor,
            'tipo': 'corrida'
        })

    for d in despesas:
        atividades.append({
            'data': d.data,
            'descricao': d.descricao,
            'valor': d.valor,
            'tipo': 'despesa'
        })

    atividades.sort(key=lambda x: x['data'], reverse=True)

    return render(request, 'dashboard.html', {
        'total_corridas': total_corridas,
        'total_despesas': total_despesas,
        'lucro': lucro,
        'atividades': atividades,
        'labels': json.dumps(labels),
        'valores': json.dumps(valores),
    })

# LOGIN / LOGOUT
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuário ou senha inválidos")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# CORRIDAS
@login_required
def criar_corrida(request):
    motorista = get_motorista(request.user)

    if not motorista:
        messages.error(request, "Motorista não encontrado.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CorridaForm(request.POST)

        if form.is_valid():
            corrida = form.save(commit=False)
            corrida.motorista = motorista
            corrida.save()
            messages.success(request, "Corrida cadastrada com sucesso!")
            return redirect('listar_corridas')
        else:
            messages.error(request, "Erro ao cadastrar corrida. Verifique os campos.")
    else:
        form = CorridaForm()

    return render(request, 'corridas/form.html', {'form': form})


@login_required
def listar_corridas(request):
    motorista = get_motorista(request.user)
    corridas = Corrida.objects.filter(motorista=motorista)

    return render(request, 'corridas/listar.html', {'corridas': corridas})


@login_required
def editar_corrida(request, id):
    motorista = get_motorista(request.user)
    corrida = get_object_or_404(Corrida, id=id, motorista=motorista)

    if request.method == 'POST':
        post = request.POST.copy()

        valor = post.get('valor')
        if valor:
            valor = valor.replace('.', '').replace(',', '.')
            post['valor'] = valor

        form = CorridaForm(post, instance=corrida)

        if form.is_valid():
            corrida = form.save(commit=False)
            corrida.motorista = motorista
            corrida.save()
            messages.success(request, "Corrida atualizada com sucesso!")
            return redirect('listar_corridas')
        else:
            messages.error(request, "Erro ao atualizar corrida. Verifique os campos.")
    else:
        form = CorridaForm(instance=corrida)

    return render(request, 'corridas/form.html', {'form': form})


@login_required
def excluir_corrida(request, id):
    motorista = get_motorista(request.user)
    corrida = get_object_or_404(Corrida, id=id, motorista=motorista)

    if request.method == 'POST':
        corrida.delete()
        messages.success(request, "Corrida excluída com sucesso!")
        return redirect('listar_corridas')

    return render(request, 'corridas/confirmar_exclusao.html', {'corrida': corrida})


# DESPESAS
@login_required
def criar_despesa(request):
    motorista = get_motorista(request.user)

    if not motorista:
        messages.error(request, "Motorista não encontrado.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = DespesaForm(request.POST)

        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.motorista = motorista
            despesa.save()
            messages.success(request, "Despesa cadastrada com sucesso!")
            return redirect('listar_despesas')
        else:
            messages.error(request, "Erro ao cadastrar despesa. Verifique os campos.")
    else:
        form = DespesaForm()

    return render(request, 'despesas/form.html', {'form': form})


@login_required
def listar_despesas(request):
    motorista = get_motorista(request.user)
    despesas = Despesa.objects.filter(motorista=motorista)

    return render(request, 'despesas/listar.html', {'despesas': despesas})


@login_required
def editar_despesa(request, id):
    motorista = get_motorista(request.user)
    despesa = get_object_or_404(Despesa, id=id, motorista=motorista)

    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)

        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.motorista = motorista
            despesa.save()
            messages.success(request, "Despesa atualizada com sucesso!")
            return redirect('listar_despesas')
        else:
            messages.error(request, "Erro ao atualizar despesa. Verifique os campos.")
    else:
        form = DespesaForm(instance=despesa)

    return render(request, 'despesas/form.html', {'form': form})


@login_required
def excluir_despesa(request, id):
    motorista = get_motorista(request.user)
    despesa = get_object_or_404(Despesa, id=id, motorista=motorista)

    if request.method == 'POST':
        despesa.delete()
        messages.success(request, "Despesa excluída com sucesso!")
        return redirect('listar_despesas')

    return render(request, 'despesas/confirmar_exclusao.html', {'despesa': despesa})

# CADASTRO
def cadastro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmar = request.POST.get("confirmar")

        if password != confirmar:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'cadastro.html')

        if len(password) < 6:
            messages.error(request, "A senha deve ter pelo menos 6 caracteres.")
            return render(request, 'cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Esse usuário já existe.")
            return render(request, 'cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Esse e-mail já está cadastrado.")
            return render(request, 'cadastro.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        Motorista.objects.create(usuario=user)

        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect('login')

    return render(request, 'cadastro.html')


# CADASTRO
def cadastro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmar = request.POST.get("confirmar")

        if password != confirmar:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'cadastro.html')

        if len(password) < 6:
            messages.error(request, "A senha deve ter pelo menos 6 caracteres.")
            return render(request, 'cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Esse usuário já existe.")
            return render(request, 'cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Esse e-mail já está cadastrado.")
            return render(request, 'cadastro.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        Motorista.objects.create(usuario=user)

        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect('login')

    return render(request, 'cadastro.html')


# HOME
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')