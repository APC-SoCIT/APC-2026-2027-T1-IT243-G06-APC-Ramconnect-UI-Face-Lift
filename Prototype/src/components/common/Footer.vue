<template>
  <footer class="bg-apc-navy text-slate-300 border-t border-white/10 mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Brand Info -->
        <div class="md:col-span-2 space-y-4">
          <div class="flex items-center space-x-3">
            <div class="w-9 h-9 rounded-full bg-apc-gold text-apc-navy flex items-center justify-center font-black text-sm">
              APC
            </div>
            <div>
              <h3 class="text-white font-bold text-base">Asia Pacific College</h3>
              <p class="text-xs text-apc-gold font-medium">Real Projects. Real Learning.</p>
            </div>
          </div>
          <p class="text-xs text-slate-300 max-w-md leading-relaxed">
            Asia Pacific College is an educational partnership between IBM Philippines and the SM Foundation. Offering industry-certified programs in Computing, Engineering, Multimedia Arts, and Business Analytics.
          </p>
          <p class="text-xs text-slate-400">
            3 Humabon St., Magallanes, Makati City, Metro Manila, Philippines 1232
          </p>
        </div>

        <!-- Quick Links -->
        <div>
          <h4 class="text-white font-semibold text-xs tracking-wider uppercase mb-3 text-apc-gold">Admissions Portal</h4>
          <ul class="space-y-2 text-xs">
            <li><router-link to="/inquire" class="hover:text-white transition-colors">Inquire Online</router-link></li>
            <li><router-link to="/apply" class="hover:text-white transition-colors">Apply for AY 2026-2027</router-link></li>
            <li><router-link to="/portal" class="hover:text-white transition-colors">Applicant Status Portal</router-link></li>
            <li><router-link to="/login" class="hover:text-white transition-colors">Sign In / Account Access</router-link></li>
          </ul>
        </div>

        <!-- Institutional Links -->
        <div>
          <h4 class="text-white font-semibold text-xs tracking-wider uppercase mb-3 text-apc-gold">Institutional</h4>
          <ul class="space-y-2 text-xs">
            <li><a href="https://apc.edu.ph" target="_blank" class="hover:text-white transition-colors">Official APC Website</a></li>
            <li><a href="https://apc.edu.ph/scholarships" target="_blank" class="hover:text-white transition-colors">Scholarships & Grants</a></li>
            <li><a href="https://apc.edu.ph/academic-calendar" target="_blank" class="hover:text-white transition-colors">Academic Calendar</a></li>
            <li><router-link to="/staff" class="hover:text-apc-gold transition-colors font-medium">Staff & Admissions Login</router-link></li>
          </ul>
        </div>
      </div>

      <div class="mt-8 pt-6 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-3">
        <p>© 2026-2027 Asia Pacific College. All rights reserved.</p>
        <div class="flex items-center space-x-4">
          <span class="hover:text-slate-300 cursor-pointer">Data Privacy Notice (R.A. 10173)</span>
          <span>•</span>
          <span class="hover:text-slate-300 cursor-pointer">Terms & Conditions</span>
        </div>
      </div>
    </div>
  </footer>
</template>
