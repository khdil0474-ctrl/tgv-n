# AI Darslar Bot

Telegram bot: majburiy obuna, bosqichma-bosqich menyular, admin panel (post qo'shish, statistika),
yangi foydalanuvchi haqida adminga avtomatik bildirishnoma.

## 1. Botni sozlash (BotFather)

Token allaqachon `config.py` ichida bor:
`8258790417:AAGJ__XEzSc_cP938-DdQxCJYEb_Joa4LlI`

Agar xohlasangiz, Railway'da **Variables** bo'limiga `BOT_TOKEN` nomi bilan yangi token qo'yib,
o'zgartirishingiz mumkin — kod avtomatik shuni ishlatadi.

## 2. MUHIM: Botni kanallarga ADMIN qilib qo'shing

Majburiy obunani tekshirish ishlashi uchun bot quyidagi 5 ta kanalning barchasiga
**admin** qilib qo'shilishi SHART (kamida "obunachilarni ko'rish" huquqi bilan):

- @sunniyintellekt_darslar
- @AIGURUH
- @xonfirestream
- @AI_YANGILIKLA
- @shoxona_kinolar

Agar bot kanalda admin bo'lmasa, u foydalanuvchining obuna holatini bila olmaydi va
xato bo'lib, foydalanuvchi "obuna bo'lmagan" deb hisoblanaveradi.

## 3. GitHub'ga yuklash

```bash
git init
git add .
git commit -m "AI darslar bot"
git branch -M main
git remote add origin https://github.com/<username>/<repo-nomi>.git
git push -u origin main
```

## 4. Railway'ga deploy qilish

1. https://railway.app ga kiring, **New Project → Deploy from GitHub repo** tanlang.
2. Yuqorida yuklagan repository'ni tanlang.
3. Railway avtomatik `requirements.txt` orqali kutubxonalarni o'rnatadi va
   `Procfile` orqali `python main.py` buyrug'ini ishga tushiradi.
4. Agar kerak bo'lsa, **Settings → Deploy → Custom Start Command** ga
   `python main.py` deb yozing.
5. **Variables** bo'limida xohlasangiz `BOT_TOKEN` va `ADMIN_ID` qo'shishingiz mumkin
   (qo'shmasangiz ham, standart qiymatlar ishlaydi).
6. Deploy tugagach, botga Telegram'da `/start` yozib tekshiring.

**Eslatma:** SQLite bazasi (`bot.db`) konteyner qayta deploy qilinganda
(masalan yangi commit push qilinganda) o'chib ketishi mumkin, chunki Railway'ning
oddiy fayl tizimi doimiy (persistent) emas. Foydalanuvchilar va postlar doim saqlanib
qolishi uchun Railway'da **Volume** qo'shib, `DB_PATH` ni shu volume ichidagi
yo'lga (masalan `/data/bot.db`) yo'naltirish tavsiya etiladi.

## 5. Admin panel qanday ishlaydi

Faqat admin (ID: `8969109663`, @auwsn) uchun:

- `/admin` — admin panelni ochadi.
- **➕ Post/Tugma qo'shish** — bosilganda bot "qaysi tugmaga qo'shamiz?" deb so'raydi,
  siz kerakli bo'limni tanlaysiz, so'ng matn/rasm/video/fayl yuborasiz — shu bo'lim uchun
  saqlanadi va foydalanuvchilarga o'sha tugma bosilganda ko'rsatiladi.
- **📊 Statistika** — jami va bugungi foydalanuvchilar sonini ko'rsatadi.

Yangi foydalanuvchi (obunani birinchi marta tasdiqlagan kishi) botga qo'shilganda,
adminga avtomatik xabar keladi: ismi, username'i, ID'si va "botning nechinchi
foydalanuvchisi" ekani.

## 6. Menyu tuzilishi

```
🏠 Bosh menyu
├── 🎓 AI TO'LIQ DARS
│   ├── 🖼 Rasm generatsiya qilish
│   └── 🎬 Rasmdan video yasash
├── 📝 Promptlar
│   ├── 🖼 Rasm referensa qilish prompti
│   ├── ✨ Sifatli rasm generatsiya prompti
│   ├── 🔍 Rasmni 4K tiniq qilish prompti
│   ├── 🌐 Sayt yasash prompti
│   └── 🤖 Bot yasash prompti
├── 🌐 Web sayt yasash
│   └── 🌐 AI orqali sayt yasash
├── 🤖 Bot yasash
│   └── 🤖 AI orqali bot yasash
└── 📞 Aloqaga chiqish (@auwsn ga link)
```

Har bir ichki tugma (masalan "Rasm generatsiya qilish") — admin tomonidan post
qo'shilishi kerak bo'lgan alohida bo'lim. Post qo'shilmagan bo'limga foydalanuvchi
kirsa, "hozircha material qo'shilmagan" degan xabar chiqadi.
