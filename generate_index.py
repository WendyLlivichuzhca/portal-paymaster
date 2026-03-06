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
    <title>Paymaster - Portal de Usuario Premium</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --primary: #3b82f6;
            --secondary: #10b981;
            --accent: #f59e0b;
            --bg-dark: #020617;
            --card-glass: rgba(15, 23, 42, 0.6);
            --border-glass: rgba(255, 255, 255, 0.1);
        }

        body { 
            font-family: 'Outfit', sans-serif; 
            background: var(--bg-dark); 
            color: #f8fafc; 
            min-height: 100vh;
            overflow-x: hidden;
            margin: 0;
        }

        .animated-mesh {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
            background: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0, transparent 50%), 
                radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.1) 0, transparent 50%),
                radial-gradient(at 50% 100%, rgba(245, 158, 11, 0.05) 0, transparent 50%);
            animation: mesh-move 20s ease infinite alternate;
        }

        @keyframes mesh-move {
            0% { transform: scale(1); }
            100% { transform: scale(1.1); }
        }

        .glass-panel { 
            background: var(--card-glass); 
            backdrop-filter: blur(24px); 
            border: 1px solid var(--border-glass);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        .glass-card { 
            background: rgba(255, 255, 255, 0.03); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .glass-card:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
        }

        .gradient-text {
            background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .btn-primary {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        }

        .animate-in {
            animation: slide-up 0.8s cubic-bezier(0.2, 0.8, 0.4, 1) forwards;
        }

        @keyframes slide-up {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-dark); }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #334155; }
    </style>
</head>
<body class="flex flex-col min-h-screen">
    <div class="animated-mesh"></div>

    <!-- LOGIN SCREEN -->
    <div id="loginSection" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-slate-950 animate-in">
        <div class="w-full max-w-lg">
            <div class="text-center mb-10">
                <div class="inline-flex p-5 bg-blue-600/10 rounded-3xl mb-6 border border-blue-500/20">
                    <i data-lucide="shield-check" class="w-16 h-16 text-blue-500"></i>
                </div>
                <h1 class="text-5xl font-black mb-3 gradient-text tracking-tighter">BIENVENIDO</h1>
                <p class="text-slate-400 text-lg font-medium">Accede a tu Portal Oficial de Paymaster</p>
            </div>

            <div class="glass-panel rounded-[2.5rem] p-10 relative overflow-hidden">
                <div class="absolute top-0 right-0 p-8 opacity-10">
                    <i data-lucide="lock" class="w-32 h-32 text-white"></i>
                </div>
                
                <div class="space-y-8 relative z-10">
                    <div class="group">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-[0.2em] mb-3 px-1 transition-colors group-focus-within:text-blue-400">Correo Electrónico</label>
                        <div class="relative">
                            <i data-lucide="mail" class="absolute left-5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500"></i>
                            <input type="email" id="loginEmail" class="w-full pl-14 pr-6 py-5 glass-card rounded-2xl outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all text-lg" placeholder="ejemplo@correo.com">
                        </div>
                    </div>

                    <div class="group">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-[0.2em] mb-3 px-1 transition-colors group-focus-within:text-blue-400">Cédula / DNI / Identificación</label>
                        <div class="relative">
                            <i data-lucide="fingerprint" class="absolute left-5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500"></i>
                            <input type="password" id="loginId" class="w-full pl-14 pr-6 py-5 glass-card rounded-2xl outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all text-lg" placeholder="••••••••••••">
                        </div>
                    </div>

                    <button id="loginBtn" class="w-full btn-primary text-white font-black py-5 rounded-2xl shadow-2xl transition-all hover:scale-[1.02] active:scale-[0.98] text-xl tracking-wide flex items-center justify-center gap-3">
                        ACCEDER AL PORTAL
                        <i data-lucide="arrow-right" class="w-6 h-6"></i>
                    </button>
                    
                    <div id="loginError" class="hidden mt-6 p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl text-center text-rose-400 text-sm font-bold animate-pulse">
                        <i data-lucide="alert-circle" class="w-4 h-4 inline mr-2"></i>
                        Datos incorrectos. Verifica tu información.
                    </div>
                </div>
            </div>
            
            <p class="mt-8 text-center text-slate-600 text-sm font-medium">
                © 2026 Paymaster Infrastructure • Asegurado con encriptación de grado militar
            </p>
        </div>
    </div>

    <!-- MAIN PORTAL -->
    <div id="portalSection" class="hidden flex w-full flex-col lg:flex-row min-h-screen">
        <!-- Persistent Sidebar -->
        <aside class="sidebar w-full lg:w-80 flex-shrink-0 flex flex-col glass-panel lg:border-r border-slate-800 lg:h-screen lg:fixed lg:left-0 lg:top-0">
            <div class="p-8">
                <div class="flex items-center gap-4 mb-12">
                    <div class="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/30">
                        <i data-lucide="zap" class="w-6 h-6 text-white"></i>
                    </div>
                    <div>
                        <span class="block font-black text-2xl tracking-tighter leading-none">PAYMASTER</span>
                        <span class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">Portal Oficial</span>
                    </div>
                </div>
                
                <nav class="space-y-3">
                    <button class="w-full flex items-center gap-4 px-6 py-4 rounded-2xl font-black transition-all bg-blue-600/10 text-blue-400 border border-blue-500/20">
                        <i data-lucide="user" class="w-5 h-5"></i> Mi Perfil
                    </button>
                    <button class="w-full flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-slate-500 hover:bg-white/5 hover:text-slate-300">
                        <i data-lucide="clipboard-list" class="w-5 h-5"></i> Mis Trámites
                    </button>
                    <button class="w-full flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-slate-500 hover:bg-white/5 hover:text-slate-300">
                        <i data-lucide="shield" class="w-5 h-5"></i> Seguridad
                    </button>
                </nav>
            </div>

            <div class="mt-auto p-8 pt-0">
                <button id="logoutBtn" class="w-full flex items-center justify-between px-6 py-4 rounded-2xl bg-slate-900 border border-slate-800 text-slate-500 hover:text-rose-400 hover:border-rose-500/30 transition-all font-black">
                    Cerrar Sesión
                    <i data-lucide="log-out" class="w-5 h-5"></i>
                </button>
            </div>
        </aside>

        <!-- Dynamic Content Area -->
        <main class="flex-1 lg:ml-80 p-4 md:p-8 lg:p-12 overflow-y-auto w-full">
            <div class="max-w-6xl mx-auto space-y-10 animate-in">
                
                <!-- Profile Identity Section -->
                <div class="glass-panel rounded-[3rem] p-8 md:p-12 relative overflow-hidden">
                    <div class="absolute -top-24 -right-24 w-96 h-96 bg-blue-600/10 rounded-full blur-[100px]"></div>
                    <div class="absolute -bottom-24 -left-24 w-96 h-96 bg-emerald-600/5 rounded-full blur-[100px]"></div>
                    
                    <div class="relative z-10 flex flex-col md:flex-row items-center md:items-end gap-10">
                        <div class="relative group">
                            <div class="w-40 h-40 rounded-[2.5rem] border-8 border-slate-900 shadow-2xl overflow-hidden ring-4 ring-blue-500/30">
                                <img src="" id="avatarImg" class="w-full h-full object-cover transition-transform group-hover:scale-110">
                            </div>
                            <div class="absolute -bottom-3 -right-3 bg-emerald-500 p-3 rounded-2xl border-4 border-slate-900 shadow-xl">
                                <i data-lucide="check" class="w-6 h-6 text-white"></i>
                            </div>
                        </div>
                        
                        <div class="flex-1 text-center md:text-left">
                            <div class="flex flex-wrap items-center justify-center md:justify-start gap-4 mb-4">
                                <h2 id="userName" class="text-4xl md:text-6xl font-black tracking-tight gradient-text leading-none">---</h2>
                                <span class="px-5 py-2 bg-blue-500/10 text-blue-400 text-xs font-black uppercase rounded-full border border-blue-500/20 tracking-tighter">
                                    Usuario Verificado
                                </span>
                            </div>
                            <div class="flex flex-wrap items-center justify-center md:justify-start gap-6 text-slate-400">
                                <div class="flex items-center gap-2">
                                    <i data-lucide="map-pin" class="w-4 h-4 text-blue-500"></i>
                                    <span id="userLocation" class="font-bold">---</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <i data-lucide="award" class="w-4 h-4 text-emerald-500"></i>
                                    <span class="font-bold">Miembro Senior</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <i data-lucide="calendar" class="w-4 h-4 text-amber-500"></i>
                                    <span class="font-bold uppercase text-[10px]">Registro: 2026</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Stats Grid -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="glass-panel p-8 rounded-[2.5rem] bg-gradient-to-br from-blue-600/10 to-transparent border-l-4 border-l-blue-500">
                        <div class="flex justify-between items-start mb-6">
                            <p class="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Aporte Voluntario</p>
                            <div class="bg-blue-500/20 p-3 rounded-2xl"><i data-lucide="dollar-sign" class="w-6 h-6 text-blue-400"></i></div>
                        </div>
                        <h3 id="profAmount" class="text-5xl font-black text-blue-400 tracking-tight">$ 0.00</h3>
                        <p class="text-xs text-slate-500 mt-4 font-medium italic">Monto total registrado en el sistema</p>
                    </div>

                    <div class="glass-panel p-8 rounded-[2.5rem] bg-gradient-to-br from-emerald-600/10 to-transparent border-l-4 border-l-emerald-500">
                        <div class="flex justify-between items-start mb-6">
                            <p class="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Estado Operativo</p>
                            <div class="bg-emerald-500/20 p-3 rounded-2xl"><i data-lucide="activity" class="w-6 h-6 text-emerald-400"></i></div>
                        </div>
                        <h3 class="text-5xl font-black text-emerald-400 tracking-tight">ACTIVO</h3>
                        <p class="text-xs text-slate-500 mt-4 font-medium italic">Tu cuenta está en pleno funcionamiento</p>
                    </div>

                    <div class="glass-panel p-8 rounded-[2.5rem] bg-gradient-to-br from-amber-600/10 to-transparent border-l-4 border-l-amber-500">
                        <div class="flex justify-between items-start mb-6">
                            <p class="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Proyectos Activos</p>
                            <div class="bg-amber-500/20 p-3 rounded-2xl"><i data-lucide="folder" class="w-6 h-6 text-amber-400"></i></div>
                        </div>
                        <h3 class="text-5xl font-black text-amber-400 tracking-tight">01</h3>
                        <p class="text-xs text-slate-500 mt-4 font-medium italic">Formulario General 2026 completado</p>
                    </div>
                </div>

                <!-- Detailed Info Grid -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
                    <!-- Contact Column -->
                    <div class="space-y-6">
                        <div class="flex items-center gap-3 px-2">
                            <i data-lucide="user-plus" class="w-5 h-5 text-blue-500"></i>
                            <h4 class="text-sm font-black uppercase tracking-[0.3em] text-slate-400">Información de Contacto</h4>
                        </div>
                        <div class="glass-card p-4 rounded-3xl flex items-center gap-5">
                            <div class="w-14 h-14 bg-slate-900 rounded-2xl flex items-center justify-center border border-slate-800"><i data-lucide="mail" class="w-5 h-5 text-blue-400"></i></div>
                            <div class="overflow-hidden">
                                <p class="text-[10px] font-black text-slate-600 uppercase mb-1">Email Principal</p>
                                <p id="profEmail" class="font-bold text-slate-200 truncate">---</p>
                            </div>
                        </div>
                        <div class="glass-card p-4 rounded-3xl flex items-center gap-5">
                            <div class="w-14 h-14 bg-slate-900 rounded-2xl flex items-center justify-center border border-slate-800"><i data-lucide="at-sign" class="w-5 h-5 text-blue-400"></i></div>
                            <div class="overflow-hidden">
                                <p class="text-[10px] font-black text-slate-600 uppercase mb-1">Email Alternativo</p>
                                <p id="profEmailAlt" class="font-bold text-slate-200 truncate">---</p>
                            </div>
                        </div>
                        <div class="glass-card p-4 rounded-3xl flex items-center gap-5">
                            <div class="w-14 h-14 bg-slate-900 rounded-2xl flex items-center justify-center border border-slate-800"><i data-lucide="phone" class="w-5 h-5 text-emerald-400"></i></div>
                            <div>
                                <p class="text-[10px] font-black text-slate-600 uppercase mb-1">Teléfono Móvil</p>
                                <p id="profPhone" class="font-bold text-slate-200">---</p>
                            </div>
                        </div>
                        <div class="glass-card p-4 rounded-3xl flex items-center gap-5">
                            <div class="w-14 h-14 bg-slate-900 rounded-2xl flex items-center justify-center border border-slate-800"><i data-lucide="send" class="w-5 h-5 text-sky-400"></i></div>
                            <div>
                                <p class="text-[10px] font-black text-slate-600 uppercase mb-1">Telegram Handle</p>
                                <p id="profUsername" class="font-bold text-slate-200">---</p>
                            </div>
                        </div>
                    </div>

                    <!-- Banking Column -->
                    <div class="space-y-6">
                        <div class="flex items-center gap-3 px-2">
                            <i data-lucide="landmark" class="w-5 h-5 text-emerald-500"></i>
                            <h4 class="text-sm font-black uppercase tracking-[0.3em] text-slate-400">Detalles de Transferencia</h4>
                        </div>
                        <div class="glass-panel rounded-[2rem] p-8 space-y-8">
                            <div class="grid grid-cols-2 gap-8">
                                <div>
                                    <p class="text-[10px] font-black text-slate-600 uppercase mb-2">Entidad Bancaria</p>
                                    <p id="profBank" class="text-lg font-black text-emerald-400">---</p>
                                    <p id="profAgency" class="text-xs font-bold text-slate-500 mt-1">Agencia: ---</p>
                                </div>
                                <div>
                                    <p class="text-[10px] font-black text-slate-600 uppercase mb-2">Tipo de Cuenta</p>
                                    <p id="profAccountType" class="text-lg font-black text-slate-200 uppercase">---</p>
                                </div>
                            </div>
                            
                            <div class="pt-6 border-t border-slate-800">
                                <p class="text-[10px] font-black text-slate-600 uppercase mb-3">Número de Cuenta Registrado</p>
                                <div class="bg-slate-950 p-4 rounded-2xl border border-slate-800 flex items-center justify-between group">
                                    <span id="profAccount" class="font-mono text-xl font-black text-emerald-500 tracking-wider">---</span>
                                    <button class="p-2 hover:bg-white/5 rounded-xl transition-colors opacity-40 group-hover:opacity-100">
                                        <i data-lucide="copy" class="w-4 h-4 text-emerald-400"></i>
                                    </button>
                                </div>
                            </div>

                            <div class="pt-2">
                                <p class="text-[10px] font-black text-slate-600 uppercase mb-3 px-1">Código SWIFT / IBAN</p>
                                <div id="profSwift" class="px-5 py-3 glass-card rounded-2xl font-mono text-sm font-bold text-blue-400 inline-block">
                                    ---
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Footer Info -->
                <div class="mt-12 text-center py-10 border-t border-slate-800">
                    <p class="text-slate-600 text-[10px] font-black uppercase tracking-[0.4em]">Fin del Portal • Información Confidencial</p>
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
            
            // Re-render only needed if body has overflow hidden
            document.body.style.overflow = 'auto';

            // Mapping Data to UI
            document.getElementById('userName').innerText = user.name;
            document.getElementById('userLocation').innerText = user.country;
            document.getElementById('profEmail').innerText = user.email_full || user.email;
            document.getElementById('profEmailAlt').innerText = user.email_alt || 'No registra';
            document.getElementById('profPhone').innerText = user.phone || 'No registra';
            document.getElementById('profUsername').innerText = user.username || 'No registra';
            document.getElementById('profBank').innerText = user.bank || '---';
            document.getElementById('profAgency').innerText = `Agencia: ${user.agency || '---'}`;
            document.getElementById('profAccountType').innerText = user.type || 'Ahorros';
            document.getElementById('profAccount').innerText = user.account || '---';
            document.getElementById('profSwift').innerText = user.swift || 'N/A';
            document.getElementById('profAmount').innerText = `$ ${user.amount}`;

            // Avatar logic
            const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=2563eb&color=fff&size=512&bold=true`;
            document.getElementById('avatarImg').src = avatarUrl;

            lucide.createIcons();
        }

        loginBtn.addEventListener('click', () => {
            const email = loginEmail.value.trim().toLowerCase();
            const id = loginId.value.trim();
            const user = DATA.find(u => (u.email === email || u.email_full?.toLowerCase() === email || u.email_alt?.toLowerCase() === email) && u.id.toString() === id);
            
            if (user) {
                localStorage.setItem('paymaster_session', user.id);
                initPortal(user);
            } else {
                loginError.classList.remove('hidden');
            }
        });

        // Logout
        document.getElementById('logoutBtn').addEventListener('click', () => {
            localStorage.removeItem('paymaster_session');
            window.location.reload();
        });

        // Session recovery
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
