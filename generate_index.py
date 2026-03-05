import json
import codecs

def generate():
    try:
        # Load the full data
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Process data for the portal
        # We include more fields now for the Profile view
        processed_data = []
        for r in data:
            item = {
                'email': str(r.get('CORREO', '')).strip().lower(),
                'name': str(r.get('NOMBRE', '')).strip(),
                'id': str(r.get('CEDULA/DNI', '')).strip(),
                'phone': str(r.get('TELEFONO', '')).strip(),
                'username': str(r.get('USUARIO', '')).strip(),
                'bank': str(r.get('BANCO', '')).strip(),
                'country': str(r.get('PAIS', '')).strip(),
                'agency': str(r.get('AGENCIA', '')).strip() if r.get('AGENCIA') else 'N/A',
                'swift': str(r.get('SWIFT/IBAN', '')).strip(),
                'account': str(r.get('CUENTA', '')).strip(),
                'type': str(r.get('TIPO', '')).strip(),
                'amount': str(r.get('MONTO', '')).strip()
            }
            # Add secondary email if it exists and is different
            email2 = str(r.get('CORREO.1', '')).strip().lower()
            if email2 and email2 != item['email']:
                item['email2'] = email2
                
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
                <div id="contentProfile" class="grid grid-cols-1 xl:grid-cols-2 gap-12 animate-enter">
                    <!-- Left: Profile Info -->
                    <div>
                        <h2 class="text-xs font-black text-slate-500 uppercase tracking-[0.2em] mb-8">Profile Info</h2>
                        <div class="flex items-center gap-6 mb-10">
                            <div class="w-24 h-24 rounded-full border-4 border-blue-600/30 p-1">
                                <img src="https://ui-avatars.com/api/?name=User&background=2563eb&color=fff&size=200" id="avatarImg" class="w-full h-full rounded-full object-cover shadow-2xl">
                            </div>
                            <div>
                                <h1 id="userName" class="text-3xl font-black mb-1">Nombre Usuario</h1>
                                <p id="userRole" class="text-blue-400 font-bold text-sm">Miembro Registrado</p>
                                <p id="userLocation" class="text-slate-500 text-xs font-medium uppercase mt-1">País, Ciudad</p>
                            </div>
                        </div>

                        <div class="space-y-4">
                            <div class="glass-card p-5 rounded-2xl flex items-center gap-4">
                                <div class="bg-blue-600/20 p-3 rounded-xl"><i data-lucide="mail" class="w-5 h-5 text-blue-400"></i></div>
                                <div>
                                    <p class="text-[10px] text-slate-500 font-bold uppercase">Email</p>
                                    <p id="profEmail" class="font-bold">---</p>
                                </div>
                            </div>
                            <div class="glass-card p-5 rounded-2xl flex items-center gap-4">
                                <div class="bg-purple-600/20 p-3 rounded-xl"><i data-lucide="phone" class="w-5 h-5 text-purple-400"></i></div>
                                <div>
                                    <p class="text-[10px] text-slate-500 font-bold uppercase">Phone</p>
                                    <p id="profPhone" class="font-bold">---</p>
                                </div>
                            </div>
                             <div class="glass-card p-5 rounded-2xl flex items-center gap-4">
                                <div class="bg-emerald-600/20 p-3 rounded-xl"><i data-lucide="landmark" class="w-5 h-5 text-emerald-400"></i></div>
                                <div>
                                    <p class="text-[10px] text-slate-500 font-bold uppercase">Banking</p>
                                    <p id="profBankInfo" class="font-bold">---</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right: Registered Projects -->
                    <div>
                        <h2 class="text-xs font-black text-slate-500 uppercase tracking-[0.2em] mb-8">Registered Projects</h2>
                        <div class="space-y-4" id="projectList">
                            <!-- Project Item -->
                            <div class="glass-card p-6 rounded-2xl flex items-center justify-between border-l-4 border-emerald-500">
                                <div>
                                    <h4 class="font-bold text-lg">Formulario Total 2026</h4>
                                    <p class="text-xs text-slate-500">Registro verificado por Paymaster</p>
                                </div>
                                <span class="px-3 py-1 bg-emerald-500/20 text-emerald-400 text-[10px] font-black uppercase rounded-lg border border-emerald-500/30">Completed</span>
                            </div>
                            <div class="glass-card p-6 rounded-2xl flex items-center justify-between border-l-4 border-amber-500 opacity-50">
                                <div>
                                    <h4 class="font-bold text-lg">Próximos Proyectos</h4>
                                    <p class="text-xs text-slate-500">Esperando convocatoria</p>
                                </div>
                                <span class="px-3 py-1 bg-amber-500/20 text-amber-400 text-[10px] font-black uppercase rounded-lg border border-amber-500/30">Pending</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bottom Summary -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 animate-enter" style="animation-delay: 0.2s">
                <div class="gradient-blue p-8 rounded-[2rem] shadow-xl shadow-blue-900/20">
                    <p class="text-blue-100/60 text-xs font-black uppercase mb-1">Total Monto</p>
                    <h3 id="statTotal" class="text-4xl font-black">$ 0.00</h3>
                </div>
                <div class="glass-panel p-8 rounded-[2rem]">
                    <p class="text-slate-500 text-xs font-black uppercase mb-1">Active Projects</p>
                    <h3 class="text-4xl font-black">1</h3>
                </div>
                <div class="gradient-green p-8 rounded-[2rem] shadow-xl shadow-emerald-900/20">
                    <p class="text-emerald-100/60 text-xs font-black uppercase mb-1">Status</p>
                    <h3 class="text-4xl font-black uppercase">Active</h3>
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
            
            document.getElementById('userName').innerText = user.name;
            document.getElementById('profEmail').innerText = user.email;
            document.getElementById('profPhone').innerText = user.phone;
            document.getElementById('profBankInfo').innerText = `${user.bank} - ${user.account}`;
            document.getElementById('userLocation').innerText = `${user.country}`;
            document.getElementById('statTotal').innerText = `$ ${user.amount}`;
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
