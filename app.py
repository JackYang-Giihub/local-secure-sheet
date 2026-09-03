#!/usr/bin/env python3
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
from secure_sheet import read_table, transform_many, encrypt_text, decrypt_text

class App:
    def __init__(self, root):
        self.root=root; root.title('本地安全表格工具'); root.geometry('700x610'); root.minsize(620,520)
        self.files=[]; self.vars=[]; self.password=tk.StringVar(); self.status=tk.StringVar(value='请选择文件')
        self.build()
    def build(self):
        m=ttk.Frame(self.root,padding=24); m.pack(fill='both',expand=True)
        ttk.Label(m,text='本地安全表格工具',font=('Arial',20,'bold')).pack(anchor='w')
        ttk.Label(m,text='批量处理 Excel / CSV / TXT，支持字段选择和单条文本',foreground='#666').pack(anchor='w',pady=(4,18))
        nb=ttk.Notebook(m); nb.pack(fill='both',expand=True)
        self.file_tab=ttk.Frame(nb,padding=12); self.text_tab=ttk.Frame(nb,padding=12); nb.add(self.file_tab,text='文件加密 / 解密'); nb.add(self.text_tab,text='单条文本')
        self.build_file_tab(); self.build_text_tab()
    def build_file_tab(self):
        t=self.file_tab; bar=ttk.Frame(t); bar.pack(fill='x')
        ttk.Button(bar,text='添加文件（可多选）',command=self.add).pack(side='left'); ttk.Button(bar,text='清空',command=self.clear).pack(side='left',padx=8)
        self.listbox=tk.Listbox(t,height=5); self.listbox.pack(fill='x',pady=8)
        ttk.Label(t,text='需要处理的字段（以第一个文件的表头为准）',font=('Arial',11,'bold')).pack(anchor='w',pady=(8,6))
        self.cf=ttk.Frame(t); self.cf.pack(fill='both',expand=True); ttk.Label(self.cf,text='添加文件后加载字段',foreground='#888').pack(anchor='w')
        pw=ttk.Frame(t); pw.pack(fill='x',pady=12); ttk.Label(pw,text='密码',width=8).pack(side='left'); ttk.Entry(pw,textvariable=self.password,show='●').pack(side='left',fill='x',expand=True)
        bs=ttk.Frame(t); bs.pack(fill='x'); ttk.Button(bs,text='🔒 批量加密',command=lambda:self.run(False)).pack(side='left',fill='x',expand=True,padx=(0,5)); ttk.Button(bs,text='🔓 批量解密',command=lambda:self.run(True)).pack(side='left',fill='x',expand=True,padx=(5,0))
        ttk.Label(t,textvariable=self.status,foreground='#1769aa').pack(anchor='w',pady=(12,0))
    def build_text_tab(self):
        t=self.text_tab; ttk.Label(t,text='输入明文或 lss1: 开头的密文').pack(anchor='w'); self.text=tk.Text(t,height=12,wrap='word'); self.text.pack(fill='both',expand=True,pady=8)
        pw=ttk.Frame(t); pw.pack(fill='x'); ttk.Label(pw,text='密码',width=8).pack(side='left'); ttk.Entry(pw,textvariable=self.password,show='●').pack(side='left',fill='x',expand=True)
        bs=ttk.Frame(t); bs.pack(fill='x',pady=12); ttk.Button(bs,text='🔒 加密文本',command=lambda:self.text_run(False)).pack(side='left',fill='x',expand=True,padx=(0,5)); ttk.Button(bs,text='🔓 解密文本',command=lambda:self.text_run(True)).pack(side='left',fill='x',expand=True,padx=(5,0))
    def add(self):
        fs=filedialog.askopenfilenames(filetypes=[('支持的文件','*.xlsx *.xlsm *.csv *.txt'),('所有文件','*.*')])
        if not fs:return
        self.files=list(dict.fromkeys(self.files+list(fs))); self.listbox.delete(0,'end')
        for f in self.files:self.listbox.insert('end',f)
        try:
            headers=[str(x).strip() if x is not None else '' for x in read_table(Path(self.files[0]))[0]]; [w.destroy() for w in self.cf.winfo_children()]; self.vars=[]
            for i,h in enumerate(headers):
                if h:
                    v=tk.BooleanVar(value=('手机' in h or '身份证' in h or '邮箱' in h)); ttk.Checkbutton(self.cf,text=h,variable=v).grid(row=i//3,column=i%3,sticky='w',padx=(0,30),pady=5); self.vars.append((h,v))
            self.status.set(f'已添加 {len(self.files)} 个文件')
        except Exception as e: messagebox.showerror('读取失败',str(e))
    def clear(self): self.files=[]; self.listbox.delete(0,'end')
    def run(self,decrypt):
        if not self.files:return messagebox.showwarning('提示','请先添加文件')
        cols=[h for h,v in self.vars if v.get()]; pwd=self.password.get()
        if not cols:return messagebox.showwarning('提示','请至少选择一个字段')
        if len(pwd)<8:return messagebox.showwarning('提示','密码至少需要 8 位')
        out=Path(self.files[0]).parent/('解密结果' if decrypt else '加密结果'); self.status.set('处理中，请稍候…')
        def work():
            try: outputs=transform_many(self.files,out,cols,pwd,decrypt); self.root.after(0,lambda: (self.status.set(f'完成，共处理 {len(outputs)} 个文件'),messagebox.showinfo('完成',f'结果已保存到：\n{out}')))
            except Exception as e:self.root.after(0,lambda: (self.status.set('处理失败'),messagebox.showerror('处理失败',str(e))))
        threading.Thread(target=work,daemon=True).start()
    def text_run(self,decrypt):
        v=self.text.get('1.0','end-1c'); pwd=self.password.get()
        if not v:return messagebox.showwarning('提示','请输入文本')
        if len(pwd)<8:return messagebox.showwarning('提示','密码至少需要 8 位')
        try:self.text.delete('1.0','end'); self.text.insert('1.0',decrypt_text(v,pwd) if decrypt else encrypt_text(v,pwd))
        except Exception as e:messagebox.showerror('处理失败',str(e))
if __name__=='__main__': root=tk.Tk(); App(root); root.mainloop()
