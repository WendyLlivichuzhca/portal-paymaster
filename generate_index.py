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
    <title>Paymaster - Portal de Usuario Luxury</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --primary: #3b82f6;
            --secondary: #10b981;
            --accent: #f59e0b;
            --bg-dark: #020617;
            --card-glass: rgba(15, 23, 42, 0.7);
            --border-glass: rgba(255, 255, 255, 0.08);
            --edge-highlight: rgba(255, 255, 255, 0.15);
        }

        body { 
            font-family: 'Outfit', sans-serif; 
            background: var(--bg-dark); 
            color: #f8fafc; 
            min-height: 100vh;
            overflow-x: hidden;
            margin: 0;
        }

        /* AURORA BACKGROUND */
        .aurora-bg {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
            background: radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.15), transparent 40%),
                        radial-gradient(circle at 80% 80%, rgba(16, 185, 129, 0.1), transparent 40%),
                        radial-gradient(circle at 50% 50%, rgba(245, 158, 11, 0.05), transparent 50%);
            filter: blur(80px);
            animation: aurora-move 15s ease-in-out infinite alternate;
        }

        @keyframes aurora-move {
            0% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(2%, 2%) scale(1.05); }
            100% { transform: translate(-2%, -1%) scale(1); }
        }

        /* GLASS PANEL WITH EDGE LIGHTING */
        .glass-panel { 
            background: var(--card-glass); 
            backdrop-filter: blur(32px); 
            border: 1px solid var(--border-glass);
            border-top: 1px solid var(--edge-highlight);
            border-left: 1px solid var(--edge-highlight);
            box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.7);
        }

        /* CARD POLISHING */
        .glass-card { 
            background: rgba(255, 255, 255, 0.02); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        }

        .glass-card:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--primary);
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.1);
            transform: translateY(-4px) scale(1.01);
        }

        /* PREMIUM HEADING */
        .gradient-text {
            background: linear-gradient(to bottom right, #ffffff 30%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }

        /* SHIMMER BUTTON EFFECT */
        .btn-luxury {
            position: relative;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .btn-luxury::after {
            content: '';
            position: absolute;
            top: -50%; left: -50%; width: 200%; height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: rotate(45deg);
            animation: shimmer 4s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-150%) rotate(45deg); }
            20% { transform: translateX(150%) rotate(45deg); }
            100% { transform: translateX(150%) rotate(45deg); }
        }

        .btn-luxury:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px -5px rgba(37, 99, 235, 0.5);
            filter: brightness(1.1);
        }

        /* INPUT GLOW */
        .input-glow:focus-within {
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3), 0 0 20px rgba(59, 130, 246, 0.1);
        }

        /* SECURITY ICON PULSE */
        .security-pulse {
            animation: pulse-ring 2.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes pulse-ring {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }

        .animate-in {
            animation: slide-up 1s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
        }

        @keyframes slide-up {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }

        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: var(--bg-dark); }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 5px; border: 2px solid var(--bg-dark); }
        ::-webkit-scrollbar-thumb:hover { background: #334155; }
    </style>
</head>
<body class="flex flex-col min-h-screen">
    <div class="aurora-bg"></div>

    <!-- LOGIN SCREEN -->
    <div id="loginSection" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-slate-950 animate-in">
        <div class="w-full max-w-lg">
            <div class="text-center mb-12">
                <div class="inline-flex p-6 bg-blue-600/10 rounded-[2rem] mb-8 border border-blue-500/20 relative security-pulse">
                    <div class="absolute inset-0 bg-blue-500/10 blur-xl rounded-full"></div>
                    <i data-lucide="shield-check" class="w-20 h-20 text-blue-500 relative z-10"></i>
                </div>
                <h1 class="text-6xl font-black mb-4 gradient-text tracking-tight uppercase">Bienvenido</h1>
                <p class="text-slate-400 text-xl font-light tracking-wide">Portal de Infraestructura Paymaster</p>
            </div>

            <div class="glass-panel rounded-[3rem] p-12 relative overflow-hidden group">
                <!-- Decorative background elements -->
                <div class="absolute -top-24 -right-24 w-48 h-48 bg-blue-500/10 rounded-full blur-3xl transition-transform group-hover:scale-150 duration-700"></div>
                
                <div class="space-y-10 relative z-10">
                    <div class="input-glow rounded-2xl transition-all">
                        <label class="block text-[10px] font-black text-slate-500 uppercase tracking-[0.3em] mb-4 px-2">Credencial de Acceso</label>
                        <div class="relative group/field">
                            <i data-lucide="mail" class="absolute left-6 top-1/2 -translate-y-1/2 w-6 h-6 text-slate-500 transition-colors group-focus-within/field:text-blue-500"></i>
                            <input type="email" id="loginEmail" class="w-full pl-16 pr-8 py-6 glass-card rounded-2xl outline-none text-lg placeholder:text-slate-600" placeholder="usuario@paymaster.com">
                        </div>
                    </div>

                    <div class="input-glow rounded-2xl transition-all">
                        <label class="block text-[10px] font-black text-slate-500 uppercase tracking-[0.3em] mb-4 px-2">Identificación Personal</label>
                        <div class="relative group/field">
                            <i data-lucide="lock" class="absolute left-6 top-1/2 -translate-y-1/2 w-6 h-6 text-slate-500 transition-colors group-focus-within/field:text-blue-500"></i>
                            <input type="password" id="loginId" class="w-full pl-16 pr-8 py-6 glass-card rounded-2xl outline-none text-lg placeholder:text-slate-600" placeholder="••••••••••••">
                        </div>
                    </div>

                    <button id="loginBtn" class="w-full btn-luxury text-white font-black py-6 rounded-2xl shadow-2xl text-xl tracking-widest flex items-center justify-center gap-4 group">
                        ACCEDER AL TERMINAL
                        <i data-lucide="chevron-right" class="w-6 h-6 transition-transform group-hover:translate-x-1"></i>
                    </button>
                    
                    <div id="loginError" class="hidden mt-6 p-5 bg-rose-500/10 border border-rose-500/20 rounded-2xl text-center text-rose-400 text-sm font-black animate-pulse">
                        <i data-lucide="shield-alert" class="w-5 h-5 inline mr-3"></i>
                        Acceso denegado. Verifique sus credenciales.
                    </div>
                </div>
            </div>
            
            <p class="mt-12 text-center text-slate-600 text-[10px] font-black uppercase tracking-[0.5em]">
                Secure Encryption • Infrastructure Level 4
            </p>
        </div>
    </div>

    <!-- MAIN PORTAL -->
    <div id="portalSection" class="hidden flex w-full flex-col lg:flex-row min-h-screen">
        <!-- Persistent Sidebar -->
        <aside class="sidebar w-full lg:w-80 flex-shrink-0 flex flex-col glass-panel lg:h-screen lg:fixed lg:left-0 lg:top-0 border-none rounded-none">
            <div class="p-10">
                <div class="flex items-center gap-5 mb-16">
                    <div class="w-14 h-14 bg-blue-600 rounded-3xl flex items-center justify-center shadow-2xl shadow-blue-500/40 relative group">
                        <div class="absolute inset-0 bg-blue-400 blur-lg opacity-0 group-hover:opacity-40 transition-opacity"></div>
                        <i data-lucide="layout-grid" class="w-7 h-7 text-white relative z-10"></i>
                    </div>
                    <div>
                        <span class="block font-black text-2xl tracking-tighter leading-none gradient-text">PAYMASTER</span>
                        <span class="text-[9px] font-black text-slate-500 uppercase tracking-[0.3em] mt-1.5 block">Infrastructure</span>
                    </div>
                </div>
                
                <nav class="space-y-4">
                    <button class="w-full flex items-center gap-5 px-8 py-5 rounded-3xl font-black transition-all bg-blue-600/10 text-blue-400 border border-blue-500/20 shadow-inner">
                        <i data-lucide="user-check" class="w-5 h-5"></i> Mi Perfil
                    </button>
                    <button class="w-full flex items-center gap-5 px-8 py-5 rounded-3xl font-bold transition-all text-slate-500 hover:bg-white/5 hover:text-slate-200">
                        <i data-lucide="database" class="w-5 h-5"></i> Archivos
                    </button>
                    <button class="w-full flex items-center gap-5 px-8 py-5 rounded-3xl font-bold transition-all text-slate-500 hover:bg-white/5 hover:text-slate-200">
                        <i data-lucide="fingerprint" class="w-5 h-5"></i> Seguridad
                    </button>
                </nav>
            </div>

            <div class="mt-auto p-10">
                <button id="logoutBtn" class="w-full flex items-center justify-between px-8 py-5 rounded-3xl bg-slate-900/50 border border-slate-800 text-slate-500 hover:text-rose-400 hover:border-rose-500/30 transition-all font-black group">
                    Desconectar
                    <i data-lucide="power" class="w-5 h-5 group-hover:rotate-12 transition-transform"></i>
                </button>
            </div>
        </aside>

        <!-- Dynamic Content Area -->
        <main class="flex-1 lg:ml-80 p-6 md:p-10 lg:p-16 overflow-y-auto w-full">
            <div class="max-w-6xl mx-auto space-y-12 animate-in">
                
                <!-- Profile Identity Section -->
                <div class="glass-panel rounded-[4rem] p-10 md:p-16 relative overflow-hidden group">
                    <div class="absolute -top-32 -right-32 w-[30rem] h-[30rem] bg-blue-600/10 rounded-full blur-[120px] group-hover:bg-blue-600/20 transition-colors duration-1000"></div>
                    
                    <div class="relative z-10 flex flex-col md:flex-row items-center md:items-end gap-12">
                        <div class="relative">
                            <div class="w-48 h-48 rounded-[3.5rem] border-[12px] border-slate-900/80 shadow-[0_0_50px_rgba(0,0,0,0.5)] overflow-hidden ring-1 ring-white/10 group-hover:scale-105 transition-transform duration-700">
                                <img src="" id="avatarImg" class="w-full h-full object-cover">
                            </div>
                            <div class="absolute -bottom-2 -right-2 bg-emerald-500 p-4 rounded-3xl border-8 border-slate-900 shadow-2xl">
                                <i data-lucide="shield-check" class="w-7 h-7 text-white"></i>
                            </div>
                        </div>
                        
                        <div class="flex-1 text-center md:text-left space-y-6">
                            <div class="inline-flex items-center gap-4 px-6 py-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
                                <span class="w-2 h-2 bg-emerald-500 rounded-full animate-ping"></span>
                                <span class="text-[10px] font-black text-emerald-400 uppercase tracking-widest">Estado: Operativo</span>
                            </div>
                            <div class="flex flex-wrap items-center justify-center md:justify-start gap-6">
                                <h2 id="userName" class="text-5xl md:text-7xl font-black tracking-tighter gradient-text leading-tight uppercase">---</h2>
                            </div>
                            <div class="flex flex-wrap items-center justify-center md:justify-start gap-8 text-slate-500">
                                <div class="flex items-center gap-3">
                                    <i data-lucide="globe" class="w-5 h-5 text-blue-500 opacity-70"></i>
                                    <span id="userLocation" class="font-bold text-sm tracking-widest uppercase">---</span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <i data-lucide="cpu" class="w-5 h-5 text-emerald-500 opacity-70"></i>
                                    <span class="font-bold text-sm tracking-widest uppercase">Nivel Senior</span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <i data-lucide="shield" class="w-5 h-5 text-amber-500 opacity-70"></i>
                                    <span class="font-bold text-sm tracking-widest uppercase">ID: Verified</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Highlight Grid -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="glass-panel p-10 rounded-[3rem] group hover:border-blue-500/30 transition-all">
                        <div class="flex justify-between items-start mb-8">
                            <p class="text-[11px] font-black text-slate-500 uppercase tracking-[0.4em]">Asset: Capital</p>
                            <div class="bg-blue-500/10 p-4 rounded-3xl border border-blue-500/10 group-hover:bg-blue-500/20 transition-colors">
                                <i data-lucide="wallet" class="w-8 h-8 text-blue-400"></i>
                            </div>
                        </div>
                        <h3 id="profAmount" class="text-6xl font-black text-blue-400 tracking-tighter">$ 0.00</h3>
                        <p class="text-[10px] text-slate-500 mt-6 font-bold uppercase tracking-widest leading-relaxed">Monto total registrado bajo su identidad digital</p>
                    </div>

                    <div class="glass-panel p-10 rounded-[3rem] group hover:border-emerald-500/30 transition-all">
                        <div class="flex justify-between items-start mb-8">
                            <p class="text-[11px] font-black text-slate-500 uppercase tracking-[0.4em]">System: Status</p>
                            <div class="bg-emerald-500/10 p-4 rounded-3xl border border-emerald-500/10 group-hover:bg-emerald-500/20 transition-colors">
                                <i data-lucide="bar-chart-3" class="w-8 h-8 text-emerald-400"></i>
                            </div>
                        </div>
                        <h3 class="text-6xl font-black text-emerald-400 tracking-tighter uppercase">Online</h3>
                        <p class="text-[10px] text-slate-500 mt-6 font-bold uppercase tracking-widest leading-relaxed">Infraestructura verificada y actualmente activa</p>
                    </div>

                    <div class="glass-panel p-10 rounded-[3rem] group hover:border-amber-500/30 transition-all">
                        <div class="flex justify-between items-start mb-8">
                            <p class="text-[11px] font-black text-slate-500 uppercase tracking-[0.4em]">Tasks: Global</p>
                            <div class="bg-amber-500/10 p-4 rounded-3xl border border-amber-500/10 group-hover:bg-amber-500/20 transition-colors">
                                <i data-lucide="workflow" class="w-8 h-8 text-amber-400"></i>
                            </div>
                        </div>
                        <h3 class="text-6xl font-black text-amber-400 tracking-tighter">01</h3>
                        <p class="text-[10px] text-slate-500 mt-6 font-bold uppercase tracking-widest leading-relaxed">Formularios procesados con éxito total</p>
                    </div>
                </div>

                <!-- Information Grid -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
                    <div class="space-y-8">
                        <div class="flex items-center gap-4 px-4">
                            <div class="w-1 h-8 bg-blue-600 rounded-full"></div>
                            <h4 class="text-xs font-black uppercase tracking-[0.4em] text-slate-500">Communications Layer</h4>
                        </div>
                        <div class="space-y-4">
                            <div class="glass-card p-6 rounded-[2.5rem] flex items-center gap-8 group/item">
                                <div class="w-16 h-16 bg-slate-900/80 rounded-3xl flex items-center justify-center border border-white/5 group-hover/item:border-blue-500/30 transition-colors"><i data-lucide="mail" class="w-6 h-6 text-blue-500"></i></div>
                                <div class="overflow-hidden">
                                    <p class="text-[9px] font-black text-slate-600 uppercase tracking-widest mb-1.5">Primary Link</p>
                                    <p id="profEmail" class="text-lg font-black text-slate-200 truncate">---</p>
                                </div>
                            </div>
                            <div class="glass-card p-6 rounded-[2.5rem] flex items-center gap-8 group/item">
                                <div class="w-16 h-16 bg-slate-900/80 rounded-3xl flex items-center justify-center border border-white/5 group-hover/item:border-blue-500/30 transition-colors"><i data-lucide="shield-plus" class="w-6 h-6 text-blue-500"></i></div>
                                <div class="overflow-hidden">
                                    <p class="text-[9px] font-black text-slate-600 uppercase tracking-widest mb-1.5">Security Recovery</p>
                                    <p id="profEmailAlt" class="text-lg font-black text-slate-200 truncate">---</p>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-4">
                                <div class="glass-card p-6 rounded-[2.5rem] flex flex-col gap-4">
                                    <i data-lucide="smartphone" class="w-6 h-6 text-emerald-500"></i>
                                    <div>
                                        <p class="text-[9px] font-black text-slate-600 uppercase tracking-widest mb-1">Mobile</p>
                                        <p id="profPhone" class="text-sm font-black text-slate-200">---</p>
                                    </div>
                                </div>
                                <div class="glass-card p-6 rounded-[2.5rem] flex flex-col gap-4">
                                    <i data-lucide="send" class="w-6 h-6 text-sky-500"></i>
                                    <div>
                                        <p class="text-[9px] font-black text-slate-600 uppercase tracking-widest mb-1">Telegram</p>
                                        <p id="profUsername" class="text-sm font-black text-slate-200">---</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="space-y-8">
                        <div class="flex items-center gap-4 px-4">
                            <div class="w-1 h-8 bg-emerald-600 rounded-full"></div>
                            <h4 class="text-xs font-black uppercase tracking-[0.4em] text-slate-500">Financial Storage Layer</h4>
                        </div>
                        <div class="glass-panel rounded-[3.5rem] p-12 space-y-12">
                            <div class="flex justify-between items-end">
                                <div>
                                    <p class="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-3">Bank Entity</p>
                                    <p id="profBank" class="text-3xl font-black text-emerald-400 tracking-tight uppercase">---</p>
                                    <p id="profAgency" class="text-[10px] font-black text-slate-600 mt-2 uppercase">Terminal: ---</p>
                                </div>
                                <div class="text-right">
                                    <p class="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-3">Account Type</p>
                                    <p id="profAccountType" class="text-xl font-black text-slate-200 uppercase tracking-tighter">---</p>
                                </div>
                            </div>
                            
                            <div class="space-y-4">
                                <p class="text-[9px] font-black text-slate-500 uppercase tracking-widest px-1">Infrastructure Account Number</p>
                                <div class="bg-slate-950 p-6 rounded-3xl border border-white/5 flex items-center justify-between group/code shadow-2xl">
                                    <span id="profAccount" class="font-mono text-2xl font-black text-emerald-500 tracking-[0.1em]">---</span>
                                    <button class="p-3 hover:bg-emerald-500/10 rounded-2xl transition-all opacity-40 group-hover/code:opacity-100">
                                        <i data-lucide="external-link" class="w-5 h-5 text-emerald-400"></i>
                                    </button>
                                </div>
                            </div>

                            <div class="flex items-center gap-6">
                                <div class="flex-1">
                                    <p class="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-3 px-1">Routing: Swift</p>
                                    <div id="profSwift" class="px-6 py-4 glass-card rounded-2xl font-mono text-xs font-black text-blue-400 tracking-widest uppercase border-blue-500/10">
                                        ---
                                    </div>
                                </div>
                                <div class="w-20 h-20 bg-emerald-500/5 rounded-[2rem] flex items-center justify-center border border-emerald-500/10">
                                    <i data-lucide="landmark" class="w-8 h-8 text-emerald-500/50"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Footer Info -->
                <div class="mt-20 text-center py-16 border-t border-white/5">
                    <div class="inline-flex items-center gap-6 opacity-30 grayscale hover:grayscale-0 transition-all duration-700">
                        <i data-lucide="lock-keyhole" class="w-5 h-5"></i>
                        <span class="text-[9px] font-black uppercase tracking-[0.8em]">End of Terminal Connection</span>
                        <i data-lucide="shield-check" class="w-5 h-5"></i>
                    </div>
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
            document.body.style.overflow = 'auto';

            // Data Injection
            document.getElementById('userName').innerText = user.name;
            document.getElementById('userLocation').innerText = user.country;
            document.getElementById('profEmail').innerText = user.email_full || user.email;
            document.getElementById('profEmailAlt').innerText = user.email_alt || 'No Data Found';
            document.getElementById('profPhone').innerText = user.phone || 'No Data Found';
            document.getElementById('profUsername').innerText = user.username || 'Unlinked';
            document.getElementById('profBank').innerText = user.bank || '---';
            document.getElementById('profAgency').innerText = `Terminal: ${user.agency || '---'}`;
            document.getElementById('profAccountType').innerText = user.type || 'Standard';
            document.getElementById('profAccount').innerText = user.account || '---';
            document.getElementById('profSwift').innerText = user.swift || 'N/A';
            document.getElementById('profAmount').innerText = `$ ${user.amount}`;

            // High Resolution Avatar
            const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=2563eb&color=fff&size=512&bold=true&font-size=0.33`;
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

        document.getElementById('logoutBtn').addEventListener('click', () => {
            localStorage.removeItem('paymaster_session');
            window.location.reload();
        });

        // Initialize session
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
