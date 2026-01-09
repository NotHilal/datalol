# Quick Start Guide - Optimized Version

## 🚀 Running Your Optimized App

### Backend (with Gzip Compression)
```bash
cd backend
pip install -r requirements.txt  # Installs Flask-Compress
python run.py
```

**You should see**:
```
[OK] Response compression enabled (gzip)
[OK] Cache initialized: simple (in-memory)
[OK] Connected to MongoDB: lol_matches
```

### Frontend (with Lazy Loading)
```bash
cd frontend
npm install
npm start  # Development mode

# OR for production build
npm run build -- --configuration production
```

---

## ✅ What's Different Now?

### 1. **First Load is 60-70% Faster**
- Before: All 8 pages loaded at once (~900 KB)
- Now: Only Dashboard loads initially (177 KB gzipped)

### 2. **API Responses 80% Smaller**
- Gzip compression automatically applied
- 100 KB JSON → 15-20 KB compressed

### 3. **Lazy Loading in Action**
When you visit different pages:
- `/dashboard` - Loads immediately (already loaded)
- `/ml` - Loads ML module on demand (~14 KB)
- `/players` - Loads Players module on demand (~6 KB)
- `/statistics` - Loads Statistics module on demand (~3 KB)

### 4. **Smart Caching**
- Browser cache: 24 hours for static assets
- Backend cache: 5-30 minutes for API data
- Frontend cache: 5 minutes for frequently accessed data

---

## 📊 Check the Optimizations

### See Lazy Loading in Browser DevTools:
1. Open Chrome DevTools (F12)
2. Go to Network tab
3. Refresh page (Ctrl+R)
4. Notice only `main.js` and `polyfills.js` load
5. Click "ML" in navbar
6. See a new chunk file load (e.g., `95.c78e7eca305a65e9.js`)

### See Gzip Compression:
1. In Network tab, click any API request
2. Check Response Headers
3. Look for: `Content-Encoding: gzip` or `br` (brotli)

### See Bundle Sizes:
```bash
cd frontend
npm run build -- --configuration production
```

**Output will show**:
```
Initial bundle: 177.08 kB (gzipped)
Lazy chunks: 37.10 kB total (gzipped)
```

---

## 🎯 Performance Checklist

✅ Backend compression enabled
✅ Frontend lazy loading working
✅ Dashboard loads in ~1-2 seconds
✅ Pages navigate smoothly
✅ Build completes without errors
✅ All modules chunk correctly

---

## 🔥 Pro Tips

### Fastest Development Experience:
```bash
# Terminal 1: Backend
cd backend && python run.py

# Terminal 2: Frontend
cd frontend && npm start

# Open: http://localhost:4200
```

### Check Performance Metrics:
```bash
# Frontend build time and sizes
cd frontend && npm run build -- --stats-json

# Use webpack-bundle-analyzer
npm install -g webpack-bundle-analyzer
webpack-bundle-analyzer dist/lol-analytics-frontend/stats.json
```

### Clear All Caches (if needed):
```bash
# Browser: Ctrl+Shift+Delete → Clear cache
# Backend: Restart backend server
# Frontend: Ctrl+Shift+R (hard refresh)
```

---

## 📚 Related Documentation

- Full details: `PERFORMANCE_OPTIMIZATIONS.md`
- Features list: `FEATURES_IMPLEMENTATION_STATUS.md`
- API docs: `API_DOCUMENTATION.md`
- Setup guide: `SETUP_GUIDE.md`

---

## 🐛 Troubleshooting

### "Module not found" error in frontend
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Lazy loading not working
- Check browser console for errors
- Verify all `*.module.ts` files exist
- Run `npm run build` and check for errors

### Gzip not working
- Verify Flask-Compress is installed: `pip list | grep Flask-Compress`
- Check backend console for "[OK] Response compression enabled"
- Test with: `curl -H "Accept-Encoding: gzip" http://localhost:5000/api/v1/health -I`

---

**Enjoy your blazing-fast app! 🚀**
