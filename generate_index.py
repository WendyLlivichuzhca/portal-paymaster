import json
import codecs

def generate():
    try:
        # Load the full data
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Process data for the portal
        # We include ALL fields from the Excel for complete Profile view
        processed_data = []
        for r in data:
            item = {
                'email': str(r.get('Correo electrónico', '') or r.get('Dirección de correo electrónico', '')).strip().lower(),
                'name': str(r.get('Nombres y Apellidos', '')).strip(),
                'id': str(r.get('Cédula de identidad (DNI)', '')).strip(),
                'phone': str(r.get('Nro teléfono con identificador del país (+57 3809080706)', '')).strip(),
                'username': str(r.get('Usuario de telegram', '')).strip(),
                'bank': str(r.get('Nombre del banco (del País donde vives)', '')).strip(),
                'country': str(r.get('País', '')).strip(),
                'agency': str(r.get('Agencia', '')).strip() if r.get('Agencia') else 'N/A',
                'swift': str(r.get('Código Swift/IBAN', '')).strip(),
                'account': str(r.get('Número de cuenta bancaria FIAT (debe estar a tu nombre)', '')).strip(),
                'type': str(r.get('Tipo de Cuenta (Ahorros/Corriente)', '')).strip(),
                'amount': str(r.get('Monto del Aporte Voluntario (USD)', '')).strip(),
                # Additional fields for complete profile
                'email_full': str(r.get('Dirección de correo electrónico', '')).strip(),
                'email_alt': str(r.get('Correo electrónico', '')).strip()
            }

            processed_data.append(item)
        
        data_json_string = json.dumps(processed_data, ensure_ascii=False)
        
        html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Portal - Paymaster</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { 
            font-family: 'Outfit', sans-serif; 
            background: #0f172a; 
            background: radial-gradient(circle at 20% 20%, #1e1b4b 0%, #0f172a 100%);
            color: #f8fafc; 
            min-height: screen;
            margin: 0;
        }
        .bg-mesh { 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
            background: radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.1) 0, transparent 50%), 
                        radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.1) 0, transparent 50%);
        }
        .sidebar { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px); border-right: 1px solid rgba(255, 255, 255, 0.05); }
        .glass-panel { background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); }
        .glass-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); }
        .active-nav { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border-left: 3px solid #3b82f6; }
        .gradient-blue { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
        .gradient-purple { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); }
        .gradient-green { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
        .animate-enter { animation: enter 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }
        @keyframes enter { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
    </style>
</head>
<body class="flex min-h-screen overflow-x-hidden">
    <div class="bg-mesh"></div>

    <!-- LOGIN OVERLAY -->
    <div id="loginSection" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-[#0f172a] animate-enter">
        <div class="w-full max-w-md">
            <div class="text-center mb-8">
                <div class="inline-flex p-4 bg-blue-600/20 rounded-2xl mb-4">
                    <i data-lucide="shield-check" class="w-12 h-12 text-blue-500"></i>
                </div>
                <h1 class="text-4xl font-extrabold mb-2 underline decoration-blue-500 underline-offset-8">LOGIN</h1>
                <p class="text-slate-400 font-medium mt-4">Accede a tu Portal de Usuario</p>
            </div>
            <div class="glass-panel rounded-[2rem] p-8 shadow-2xl">
                <div class="space-y-6">
                    <div>
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2 px-1">Correo Electrónico</label>
                        <input type="email" id="loginEmail" class="w-full px-5 py-4 glass-card rounded-2xl outline-none focus:border-blue-500 transition-all" placeholder="ejemplo@correo.com">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2 px-1">Cédula / DNI</label>
                        <input type="password" id="loginId" class="w-full px-5 py-4 glass-card rounded-2xl outline-none focus:border-blue-500 transition-all" placeholder="••••••••">
                    </div>
                    <button id="loginBtn" class="w-full gradient-blue text-white font-bold py-4 rounded-2xl shadow-lg transition-all hover:scale-[1.02] active:scale-[0.98]">
                        ENTRAR
                    </button>
                </div>
                <div id="loginError" class="hidden mt-4 text-center text-rose-400 text-sm font-bold">Datos incorrectos. Revisa tu correo o ID.</div>
            </div>
        </div>
    </div>

    <!-- MAIN DASHBOARD (HIDDEN) -->
    <div id="portalSection" class="hidden flex w-full">
        <!-- Sidebar -->
        <aside class="sidebar w-64 flex-shrink-0 hidden lg:flex flex-col p-6">
            <div class="flex items-center gap-3 mb-12 px-2">
                <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                    <i data-lucide="hexagon" class="w-5 h-5 text-white"></i>
                </div>
                <span class="font-extrabold text-xl tracking-tight">USER PORTAL</span>
            </div>
            
            <nav class="flex-1 space-y-2">
                <button id="navProfile" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold transition-all active-nav">
                    <i data-lucide="user" class="w-5 h-5"></i> Perfil
                </button>
                <button id="navProjects" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold transition-all text-slate-400 hover:bg-white/5">
                    <i data-lucide="layout" class="w-5 h-5"></i> Proyectos
                </button>
            </nav>

            <button id="logoutBtn" class="flex items-center gap-3 px-4 py-3 text-slate-500 hover:text-rose-400 font-bold transition-all mt-auto">
                <i data-lucide="log-out" class="w-5 h-5"></i> Logout
            </button>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 p-4 lg:p-10 flex flex-col max-w-7xl mx-auto w-full">
            <!-- Topbar Mobile -->
            <div class="lg:hidden flex items-center justify-between mb-8 glass-panel p-4 rounded-2xl">
                <span class="font-black text-blue-500">PAYMASTER</span>
                <button id="mobileLogout" class="text-rose-400 p-2"><i data-lucide="log-out" class="w-6 h-6"></i></button>
            </div>

            <!-- Profile & Projects Grid -->
            <div class="glass-panel flex-1 rounded-[2.5rem] p-6 lg:p-12 overflow-y-auto mb-8 shadow-2xl">
                <!-- Two Column Layout for Desktop -->
                <div id="contentProfile" class="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-enter">
                    
                    <!-- Left Column: Profile Header & Contact (Wider) -->
                    <div class="lg:col-span-2">
                        <!-- Profile Header -->
                        <div class="mb-8">
                            <div class="flex items-end gap-6 mb-8 pb-8 border-b border-slate-600/30">
                                <div class="w-28 h-28 rounded-2xl border-4 border-blue-600/50 p-1 shadow-lg shadow-blue-600/20">
                                    <img src="https://ui-avatars.com/api/?name=User&background=2563eb&color=fff&size=200" id="avatarImg" class="w-full h-full rounded-xl object-cover">
                                </div>
                                <div class="flex-1">
                                    <div class="flex items-center gap-3 mb-2">
                                        <h1 id="userName" class="text-4xl font-black">Nombre Usuario</h1>
                                        <span class="px-3 py-1 bg-blue-500/20 text-blue-400 text-xs font-black uppercase rounded-lg border border-blue-500/30">
                                            Verificado
                                        </span>
                                    </div>
                                    <p id="userLocation" class="text-slate-400 text-sm font-medium">País</p>
                                    <p class="text-xs text-slate-500 mt-1">Miembro Registrado • Paymaster Portal</p>
                                </div>
                            </div>
                        </div>

                        <!-- Contact Information Grid -->
                        <div class="mb-8">
                            <h2 class="text-xs font-black text-slate-400 uppercase tracking-[0.15em] mb-4 flex items-center gap-2">
                                <i data-lucide="contact" class="w-4 h-4"></i>
                                Información de Contacto
                            </h2>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                                <div class="glass-card p-4 rounded-xl hover:bg-white/5 transition-all border border-slate-600/20">
                                    <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-1">Email Principal</p>
                                    <p id="profEmail" class="font-semibold text-sm text-blue-300 truncate">---</p>
                                </div>
                                <div class="glass-card p-4 rounded-xl hover:bg-white/5 transition-all border border-slate-600/20">
                                    <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-1">Email Alternativo</p>
                                    <p id="profEmailAlt" class="font-semibold text-sm text-blue-300 truncate">---</p>
                                </div>
                                <div class="glass-card p-4 rounded-xl hover:bg-white/5 transition-all border border-slate-600/20">
                                    <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-1">Teléfono</p>
                                    <p id="profPhone" class="font-semibold text-sm text-purple-300 truncate">---</p>
                                </div>
                                <div class="glass-card p-4 rounded-xl hover:bg-white/5 transition-all border border-slate-600/20">
                                    <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-1">Usuario Telegram</p>
                                    <p id="profUsername" class="font-semibold text-sm text-cyan-300 truncate">---</p>
                                </div>
                            </div>
                        </div>

                        <!-- Banking Information Card -->
                        <div>
                            <h2 class="text-xs font-black text-slate-400 uppercase tracking-[0.15em] mb-4 flex items-center gap-2">
                                <i data-lucide="landmark" class="w-4 h-4"></i>
                                Información Bancaria
                            </h2>
                            <div class="glass-card p-6 rounded-2xl border border-slate-600/30 hover:border-emerald-500/30 transition-all">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <!-- Country -->
                                    <div class="pb-4 border-b md:border-b-0 md:border-r border-slate-600/20">
                                        <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-2">País</p>
                                        <p id="profCountry" class="font-semibold text-green-300">---</p>
                                    </div>
                                    <!-- Bank -->
                                    <div class="pb-4 border-b md:border-b-0">
                                        <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-2">Banco</p>
                                        <p id="profBank" class="font-semibold text-emerald-300 truncate">---</p>
                                    </div>
                                    <!-- Agency -->
                                    <div class="pb-4 border-b md:border-b-0 md:border-r border-slate-600/20">
                                        <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-2">Agencia</p>
                                        <p id="profAgency" class="font-semibold text-teal-300 text-sm">---</p>
                                    </div>
                                    <!-- Account Type -->
                                    <div class="pb-4 border-b md:border-b-0">
                                        <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-2">Tipo de Cuenta</p>
                                        <p id="profAccountType" class="font-semibold text-orange-300">---</p>
                                    </div>
                                    <!-- Account Number -->
                                    <div class="md:col-span-2 pt-4 border-t border-slate-600/20">
                                        <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-2">Número de Cuenta</p>
                                        <p id="profAccount" class="font-mono text-sm font-semibold text-red-300 break-all">---</p>
                                    </div>
                                    <!-- Swift/IBAN -->
                                    <div class="md:col-span-2">
                                        <p class="text-[9px] text-slate-500 font-bold uppercase tracking-wide mb-2">Código Swift/IBAN</p>
                                        <p id="profSwift" class="font-mono text-sm font-semibold text-indigo-300">---</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right Column: Projects & Stats -->
                    <div class="lg:col-span-1 space-y-6">
                        
                        <!-- Amount Highlight Card -->
                        <div class="glass-card p-6 rounded-2xl bg-gradient-to-br from-yellow-500/15 to-orange-500/15 border-2 border-yellow-500/30 hover:border-yellow-500/50 transition-all shadow-lg shadow-yellow-500/10">
                            <div class="flex items-center justify-between mb-3">
                                <p class="text-[10px] text-slate-500 font-black uppercase">Aporte Económico</p>
                                <div class="bg-yellow-500/30 p-2 rounded-lg">
                                    <i data-lucide="dollar-sign" class="w-5 h-5 text-yellow-400"></i>
                                </div>
                            </div>
                            <p id="profAmount" class="text-3xl font-black text-yellow-400">$ 0.00</p>
                            <p class="text-xs text-yellow-300/70 mt-2">Monto registrado en el sistema</p>
                        </div>

                        <!-- Projects -->
                        <div>
                            <h3 class="text-xs font-black text-slate-400 uppercase tracking-[0.15em] mb-3 flex items-center gap-2">
                                <i data-lucide="folder-open" class="w-4 h-4"></i>
                                Proyectos Activos
                            </h3>
                            <div class="space-y-2">
                                <div class="glass-card p-4 rounded-xl border-l-4 border-emerald-500 bg-emerald-500/5 hover:bg-emerald-500/10 transition-all">
                                    <div class="flex items-start justify-between">
                                        <div>
                                            <h4 class="font-bold text-sm text-emerald-300">Formulario 2026</h4>
                                            <p class="text-xs text-slate-500 mt-1">Completado</p>
                                        </div>
                                        <span class="px-2 py-1 bg-emerald-500/30 text-emerald-400 text-[8px] font-black rounded border border-emerald-500/50">✓</span>
                                    </div>
                                </div>
                                <div class="glass-card p-4 rounded-xl border-l-4 border-slate-600 bg-slate-700/5 opacity-60">
                                    <div class="flex items-start justify-between">
                                        <div>
                                            <h4 class="font-bold text-sm text-slate-400">Próximos Proyectos</h4>
                                            <p class="text-xs text-slate-600 mt-1">Por confirmar</p>
                                        </div>
                                        <span class="px-2 py-1 bg-slate-600/30 text-slate-400 text-[8px] font-black rounded border border-slate-600/50">⏱</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Status Box -->
                        <div class="glass-card p-5 rounded-xl bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/30">
                            <div class="flex items-center gap-3">
                                <div class="bg-green-500/30 p-3 rounded-lg">
                                    <i data-lucide="shield-check" class="w-5 h-5 text-green-400"></i>
                                </div>
                                <div>
                                    <p class="text-[9px] text-slate-500 font-bold uppercase">Estado</p>
                                    <p class="text-sm font-black text-green-400">Activo</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bottom Summary -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 animate-enter" style="animation-delay: 0.2s">
                <div class="gradient-blue p-8 rounded-[2rem] shadow-xl shadow-blue-900/20 hover:scale-105 transition-transform">
                    <div class="flex items-center justify-between mb-4">
                        <div class="bg-white/20 p-3 rounded-xl">
                            <i data-lucide="dollar-sign" class="w-6 h-6 text-white"></i>
                        </div>
                        <div class="text-right">
                            <p class="text-blue-100/60 text-xs font-black uppercase">Total Aportado</p>
                            <h3 id="statTotal" class="text-3xl font-black">$ 0.00</h3>
                        </div>
                    </div>
                    <div class="w-full bg-white/20 rounded-full h-2">
                        <div class="bg-white h-2 rounded-full" style="width: 75%"></div>
                    </div>
                </div>
                <div class="glass-panel p-8 rounded-[2rem] hover:bg-white/5 transition-all border border-slate-600/30">
                    <div class="flex items-center justify-between mb-4">
                        <div class="bg-slate-600/30 p-3 rounded-xl">
                            <i data-lucide="folder-open" class="w-6 h-6 text-slate-400"></i>
                        </div>
                        <div class="text-right">
                            <p class="text-slate-500 text-xs font-black uppercase">Proyectos Activos</p>
                            <h3 class="text-3xl font-black">1</h3>
                        </div>
                    </div>
                    <p class="text-xs text-slate-500">Proyecto completado exitosamente</p>
                </div>
                <div class="gradient-green p-8 rounded-[2rem] shadow-xl shadow-emerald-900/20 hover:scale-105 transition-transform">
                    <div class="flex items-center justify-between mb-4">
                        <div class="bg-white/20 p-3 rounded-xl">
                            <i data-lucide="user-check" class="w-6 h-6 text-white"></i>
                        </div>
                        <div class="text-right">
                            <p class="text-emerald-100/60 text-xs font-black uppercase">Estado</p>
                            <h3 class="text-3xl font-black uppercase">Activo</h3>
                        </div>
                    </div>
                    <p class="text-xs text-emerald-100/60">Membresía verificada</p>
                </div>
            </div>
        </main>
    </div>

    <script>
        const DATA = %DATA%;
        
        const loginSection = document.getElementById('loginSection');
        const portalSection = document.getElementById('portalSection');
        const loginEmail = document.getElementById('loginEmail');
        const loginId = document.getElementById('loginId');
        const loginBtn = document.getElementById('loginBtn');
        const loginError = document.getElementById('loginError');

        function initPortal(user) {
            loginSection.classList.add('hidden');
            portalSection.classList.remove('hidden');

            // Basic info
            document.getElementById('userName').innerText = user.name;
            document.getElementById('userLocation').innerText = `${user.country}`;

            // All profile fields
            document.getElementById('profEmail').innerText = user.email_full || user.email;
            document.getElementById('profEmailAlt').innerText = user.email_alt || 'N/A';
            document.getElementById('profPhone').innerText = user.phone || 'N/A';
            document.getElementById('profUsername').innerText = user.username || 'N/A';
            document.getElementById('profCountry').innerText = user.country || 'N/A';
            document.getElementById('profBank').innerText = user.bank || 'N/A';
            document.getElementById('profAgency').innerText = user.agency || 'N/A';
            document.getElementById('profAccountType').innerText = user.type || 'N/A';
            document.getElementById('profAccount').innerText = user.account || 'N/A';
            document.getElementById('profSwift').innerText = user.swift || 'N/A';
            document.getElementById('profAmount').innerText = `$ ${user.amount}` || '$ 0.00';

            // Avatar and stats
            document.getElementById('statTotal').innerText = `$ ${user.amount}` || '$ 0.00';
            document.getElementById('avatarImg').src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=2563eb&color=fff&size=200`;

            lucide.createIcons();
        }

        loginBtn.addEventListener('click', () => {
            const email = loginEmail.value.trim().toLowerCase();
            const id = loginId.value.trim();
            const user = DATA.find(u => (u.email === email || u.email2 === email) && u.id.toString() === id);
            
            if (user) {
                localStorage.setItem('paymaster_session', user.id);
                initPortal(user);
            } else {
                loginError.innerHTML = '<i data-lucide="alert-circle" class="w-4 h-4 inline mr-2"></i> No estás registrado. Espera a que te pasemos el formulario.';
                loginError.classList.remove('hidden');
                lucide.createIcons();
            }
        });

        document.getElementById('navProjects').addEventListener('click', () => {
             alert('Sección en desarrollo: Aquí se listarán tus proyectos futuros.');
        });

        const logoutHandler = () => {
            localStorage.removeItem('paymaster_session');
            window.location.reload();
        };

        document.getElementById('logoutBtn').addEventListener('click', logoutHandler);
        document.getElementById('mobileLogout').addEventListener('click', logoutHandler);

        // Check Session
        const saved = localStorage.getItem('paymaster_session');
        if (saved) {
            const user = DATA.find(u => u.id.toString() === saved);
            if (user) initPortal(user);
        }

        lucide.createIcons();
    </script>
</body>
</html>"""
        
        # Inject data string
        final_html = html_template.replace('%DATA%', data_json_string)
        
        with codecs.open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        print("Successfully generated index.html with Portal functionality")
        
    except Exception as e:
        print(f"Error during generation: {e}")

if __name__ == "__main__":
    generate()
