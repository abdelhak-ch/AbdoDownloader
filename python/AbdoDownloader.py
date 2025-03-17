import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp

# دالة لتنزيل الفيديو أو قائمة التشغيل
def download_video():
    url = entry_url.get()
    output_path = entry_output.get()
    quality = combo_quality.get()

    if not url:
        messagebox.showerror("خطأ", "الرجاء إدخال رابط الفيديو أو قائمة التشغيل.")
        return

    if not output_path:
        messagebox.showerror("خطأ", "الرجاء تحديد مجلد الحفظ.")
        return

    # التحقق مما إذا كان الرابط لفيديو Shorts
    is_shorts = "/shorts/" in url

    # إعداد خيارات yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': quality,  # استخدام الجودة المحددة
        'progress_hooks': [update_progress],  # تحديث شريط التقدم
    }

    # إذا كان الرابط لقائمة تشغيل، قم بإنشاء مجلد خاص
    if "playlist" in url.lower():
        playlist_name = url.split("list=")[-1]
        ydl_opts['outtmpl'] = os.path.join(output_path, f'{playlist_name}/%(title)s.%(ext)s')

    try:
        progress_bar['value'] = 0
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if is_shorts:
            messagebox.showinfo("تم", "تم تنزيل فيديو Shorts بنجاح!")
        else:
            messagebox.showinfo("تم", "تم التنزيل بنجاح!")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء التنزيل: {e}")
    finally:
        progress_bar['value'] = 0

# دالة لتحديث شريط التقدم
def update_progress(d):
    if d['status'] == 'downloading':
        # استخراج النسبة المئوية من السلسلة النصية
        percent_str = d.get('_percent_str', '0%').strip('%')
        try:
            percent = float(percent_str)
            progress_bar['value'] = percent
            root.update_idletasks()
        except ValueError:
            pass  # تجاهل الأخطاء في تحويل النسبة المئوية

# دالة لاختيار مجلد الحفظ
def choose_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, folder)

# إنشاء واجهة المستخدم
root = tk.Tk()
root.title("تنزيل الفيديوهات من يوتيوب")

# تطبيق سمة حديثة
style = ttk.Style(root)
style.theme_use("clam")  # يمكنك تجربة "default" أو "alt" أيضًا

# إطار للإدخالات
frame = ttk.Frame(root, padding="10")
frame.pack(fill="both", expand=True)

# حقل إدخال الرابط
label_url = ttk.Label(frame, text="رابط الفيديو أو قائمة التشغيل:")
label_url.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_url = ttk.Entry(frame, width=50)
entry_url.grid(row=0, column=1, padx=5, pady=5)

# حقل إدخال مجلد الحفظ
label_output = ttk.Label(frame, text="مجلد الحفظ:")
label_output.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_output = ttk.Entry(frame, width=50)
entry_output.grid(row=1, column=1, padx=5, pady=5)
button_browse = ttk.Button(frame, text="تصفح", command=choose_output_folder)
button_browse.grid(row=1, column=2, padx=5, pady=5)

# قائمة الجودة
label_quality = ttk.Label(frame, text="جودة الفيديو:")
label_quality.grid(row=2, column=0, padx=5, pady=5, sticky="w")
combo_quality = ttk.Combobox(frame, values=["best", "1080p", "720p", "480p", "360p"])
combo_quality.set("best")  # القيمة الافتراضية
combo_quality.grid(row=2, column=1, padx=5, pady=5)

# شريط التقدم
progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=3, pady=10)

# زر التنزيل
button_download = ttk.Button(frame, text="تنزيل", command=download_video)
button_download.grid(row=4, column=0, columnspan=3, pady=10)

# تشغيل الواجهة
root.mainloop()