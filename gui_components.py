import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import os


class GUIComponents:
    
    def __init__(self, parent_app):
        self.app = parent_app
        self.root = parent_app.root
        self.notebook = None
        
        # Professional color scheme
        self.colors = {
            'primary': '#4A90E2',
            'secondary': '#F5F7FA',
            'text_dark': '#2C3E50',
            'text_light': '#7F8C8D',
            'border': '#D0D3D4',
            'success': '#27AE60',
            'warning': '#E67E22',
            'danger': '#E74C3C',
            'white': '#FFFFFF',
            'hover': '#5DADE2'
        }
        
        self.preview_images = {}
        
    def create_notebook(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background=self.colors['secondary'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[15, 8], 
                       font=('Segoe UI', 10),
                       background=self.colors['white'],
                       foreground=self.colors['text_dark'])
        style.map('TNotebook.Tab', 
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=0, pady=0)
        return self.notebook
    
    def create_watermarking_tab(self):
        watermarking_frame = tk.Frame(self.notebook, bg=self.colors['secondary'])
        self.notebook.add(watermarking_frame, text="  Watermarking  ")
        
        main_container = tk.Frame(watermarking_frame, bg=self.colors['secondary'])
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg=self.colors['white'], relief='flat', bd=1)
        left_panel.pack(side='left', fill='both', padx=(0, 10), pady=0)
        left_panel.configure(width=350)
        
        # Right panel - Preview
        right_panel = tk.Frame(main_container, bg=self.colors['white'], relief='flat', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # === CONTROLS ===
        selection_section = self._create_control_section(left_panel, "Image Selection")
        
        # Main image
        main_frame = tk.Frame(selection_section, bg='white')
        main_frame.pack(fill='x', pady=8, padx=15)
        
        tk.Label(main_frame, text="Main Image:", 
                font=('Segoe UI', 9), bg='white',
                fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        
        tk.Button(main_frame, text="Select Main Image", 
                 command=self.app.select_main_image,
                 bg=self.colors['primary'], fg='white',
                 font=('Segoe UI', 9, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2',
                 activebackground=self.colors['hover']).pack(fill='x')
        
        self.app.main_image_label = tk.Label(main_frame, text="No image selected",
                                             font=('Segoe UI', 8), 
                                             fg=self.colors['text_light'],
                                             bg='white', anchor='w')
        self.app.main_image_label.pack(fill='x', pady=(5, 0))
        
        # Watermark image
        watermark_frame = tk.Frame(selection_section, bg='white')
        watermark_frame.pack(fill='x', pady=8, padx=15)
        
        tk.Label(watermark_frame, text="Watermark Image:", 
                font=('Segoe UI', 9), bg='white',
                fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        
        tk.Button(watermark_frame, text="Select Watermark", 
                 command=self.app.select_watermark_image,
                 bg=self.colors['primary'], fg='white',
                 font=('Segoe UI', 9, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2',
                 activebackground=self.colors['hover']).pack(fill='x')
        
        self.app.watermark_image_label = tk.Label(watermark_frame, 
                                                  text="No watermark selected",
                                                  font=('Segoe UI', 8), 
                                                  fg=self.colors['text_light'],
                                                  bg='white', anchor='w')
        self.app.watermark_image_label.pack(fill='x', pady=(5, 0))
        
        # Settings
        settings_section = self._create_control_section(left_panel, "Watermark Settings")
        
        settings_content = tk.Frame(settings_section, bg='white')
        settings_content.pack(fill='x', pady=8, padx=15)
        
        # Type
        tk.Label(settings_content, text="Watermark Type:", 
                font=('Segoe UI', 9, 'bold'), bg='white',
                fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 8))
        
        type_frame = tk.Frame(settings_content, bg='white')
        type_frame.pack(fill='x', pady=(0, 15))
        
        tk.Radiobutton(type_frame, text="Visible (Edge Detection)", 
                      variable=self.app.watermark_type, value='visible',
                      font=('Segoe UI', 9), bg='white', 
                      fg=self.colors['text_dark'],
                      selectcolor=self.colors['primary'],
                      activebackground='white',
                      cursor='hand2').pack(anchor='w', pady=2)
        
        tk.Radiobutton(type_frame, text="Invisible (Frequency Domain)", 
                      variable=self.app.watermark_type, value='invisible',
                      font=('Segoe UI', 9), bg='white', 
                      fg=self.colors['text_dark'],
                      selectcolor=self.colors['primary'],
                      activebackground='white',
                      cursor='hand2').pack(anchor='w', pady=2)
        
        # Edge opacity
        opacity_frame = tk.Frame(settings_content, bg='white')
        opacity_frame.pack(fill='x', pady=(0, 12))
        
        opacity_label_frame = tk.Frame(opacity_frame, bg='white')
        opacity_label_frame.pack(fill='x')
        
        tk.Label(opacity_label_frame, text="Edge Opacity:", 
                font=('Segoe UI', 9), bg='white',
                fg=self.colors['text_dark']).pack(side='left')
        
        self.app.edge_opacity_label = tk.Label(opacity_label_frame, text="50",
                                               font=('Segoe UI', 9, 'bold'),
                                               bg='white', 
                                               fg=self.colors['primary'])
        self.app.edge_opacity_label.pack(side='right')
        
        self.app.edge_opacity_scale = tk.Scale(opacity_frame, from_=0, to=100,
                                              variable=self.app.edge_opacity,
                                              orient='horizontal',
                                              bg='white', 
                                              fg=self.colors['primary'],
                                              troughcolor=self.colors['secondary'],
                                              highlightthickness=0,
                                              showvalue=False,
                                              command=self.app.update_edge_opacity_label)
        self.app.edge_opacity_scale.pack(fill='x', pady=(5, 0))
        
        # Alpha
        alpha_frame = tk.Frame(settings_content, bg='white')
        alpha_frame.pack(fill='x', pady=(0, 12))
        
        alpha_label_frame = tk.Frame(alpha_frame, bg='white')
        alpha_label_frame.pack(fill='x')
        
        tk.Label(alpha_label_frame, text="Watermark Strength:", 
                font=('Segoe UI', 9), bg='white',
                fg=self.colors['text_dark']).pack(side='left')
        
        self.app.watermark_alpha_label = tk.Label(alpha_label_frame, text="0.10",
                                                  font=('Segoe UI', 9, 'bold'),
                                                  bg='white', 
                                                  fg=self.colors['primary'])
        self.app.watermark_alpha_label.pack(side='right')
        
        self.app.watermark_alpha_scale = tk.Scale(alpha_frame, from_=0.0, to=1.0,
                                                 resolution=0.01,
                                                 variable=self.app.watermark_alpha,
                                                 orient='horizontal',
                                                 bg='white', 
                                                 fg=self.colors['primary'],
                                                 troughcolor=self.colors['secondary'],
                                                 highlightthickness=0,
                                                 showvalue=False,
                                                 command=self.app.update_watermark_alpha_label)
        self.app.watermark_alpha_scale.pack(fill='x', pady=(5, 0))
        
        # Apply button
        button_frame = tk.Frame(left_panel, bg='white')
        button_frame.pack(fill='x', pady=15, padx=15)
        
        tk.Button(button_frame, text="Apply Watermark", 
                 command=self.app.apply_watermark,
                 bg=self.colors['success'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=20, pady=12, cursor='hand2',
                 activebackground='#229954').pack(fill='x')
        # === PREVIEW ===
        preview_header = tk.Frame(right_panel, bg=self.colors['primary'], height=45)
        preview_header.pack(fill='x')
        preview_header.pack_propagate(False)

        tk.Label(preview_header, text="Preview", 
                font=('Segoe UI', 11, 'bold'), fg='white', 
                bg=self.colors['primary']).pack(pady=12, padx=15, anchor='w')

        preview_content = tk.Frame(right_panel, bg='white')
        preview_content.pack(fill='both', expand=True, padx=0, pady=0)

        preview_grid = tk.Frame(preview_content, bg='white')
        preview_grid.pack(fill='both', expand=True, padx=10, pady=10)

        # Adjust grid configuration
        preview_grid.columnconfigure(0, weight=1)
        preview_grid.columnconfigure(1, weight=1)
        preview_grid.rowconfigure(0, weight=1)
        preview_grid.rowconfigure(1, weight=1)

        # Main Image (left)
        main_preview_frame = self._create_preview_box(preview_grid, "Main Image")
        main_preview_frame.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=5, pady=5)

        self.app.watermark_main_canvas = tk.Canvas(main_preview_frame, 
                                                bg=self.colors['secondary'],
                                                highlightthickness=0)
        self.app.watermark_main_canvas.pack(fill='both', expand=True, padx=5, pady=5)

        # Watermark (top-right)
        watermark_preview_frame = self._create_preview_box(preview_grid, "Watermark")
        watermark_preview_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.app.watermark_wm_canvas = tk.Canvas(watermark_preview_frame, 
                                                bg=self.colors['secondary'],
                                                highlightthickness=0)
        self.app.watermark_wm_canvas.pack(fill='both', expand=True, padx=5, pady=5)

        # Result (bottom-right)
        result_preview_frame = self._create_preview_box(preview_grid, "Result")
        result_preview_frame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

        self.app.watermark_result_canvas = tk.Canvas(result_preview_frame, 
                                                bg=self.colors['secondary'],
                                                highlightthickness=0)
        self.app.watermark_result_canvas.pack(fill='both', expand=True, padx=5, pady=5)

        
        # Status
        status_frame = tk.Frame(preview_content, bg='white', height=40)
        status_frame.pack(fill='x', padx=10)
        status_frame.pack_propagate(False)
        
        self.app.watermark_status = tk.Label(status_frame, text="Ready to process",
                                            font=('Segoe UI', 9), 
                                            fg=self.colors['text_light'],
                                            bg='white')
        self.app.watermark_status.pack(pady=10)
    
    def create_blending_tab(self):
        blending_frame = tk.Frame(self.notebook, bg=self.colors['secondary'])
        self.notebook.add(blending_frame, text="  Image Blending  ")
        
        main_container = tk.Frame(blending_frame, bg=self.colors['secondary'])
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Left panel
        left_panel = tk.Frame(main_container, bg=self.colors['white'], relief='flat', bd=1)
        left_panel.pack(side='left', fill='both', padx=(0, 10))
        left_panel.configure(width=350)
        
        # Right panel
        right_panel = tk.Frame(main_container, bg=self.colors['white'], relief='flat', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # === CONTROLS ===
        selection_section = self._create_control_section(left_panel, "Image Selection")
        
        # First image
        first_frame = tk.Frame(selection_section, bg='white')
        first_frame.pack(fill='x', pady=8, padx=15)
        
        tk.Label(first_frame, text="First Image:", 
                font=('Segoe UI', 9), bg='white',
                fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        
        tk.Button(first_frame, text="Select First Image", 
                 command=self.app.select_first_image,
                 bg=self.colors['primary'], fg='white',
                 font=('Segoe UI', 9, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2',
                 activebackground=self.colors['hover']).pack(fill='x')
        
        self.app.first_image_label = tk.Label(first_frame, text="No image selected",
                                              font=('Segoe UI', 8), 
                                              fg=self.colors['text_light'],
                                              bg='white', anchor='w')
        self.app.first_image_label.pack(fill='x', pady=(5, 0))
        
        # Second image
        second_frame = tk.Frame(selection_section, bg='white')
        second_frame.pack(fill='x', pady=8, padx=15)
        
        tk.Label(second_frame, text="Second Image:", 
                font=('Segoe UI', 9), bg='white',
                fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        
        tk.Button(second_frame, text="Select Second Image", 
                 command=self.app.select_second_image,
                 bg=self.colors['primary'], fg='white',
                 font=('Segoe UI', 9, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2',
                 activebackground=self.colors['hover']).pack(fill='x')
        
        self.app.second_image_label = tk.Label(second_frame, text="No image selected",
                                               font=('Segoe UI', 8), 
                                               fg=self.colors['text_light'],
                                               bg='white', anchor='w')
        self.app.second_image_label.pack(fill='x', pady=(5, 0))
        
        # Settings
        settings_section = self._create_control_section(left_panel, "Blending Settings")
        
        settings_content = tk.Frame(settings_section, bg='white')
        settings_content.pack(fill='x', pady=8, padx=15)
        
        # Direction
        tk.Label(settings_content, text="Blend Direction:", 
                font=('Segoe UI', 9, 'bold'), bg='white',
                fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 8))
        
        direction_frame = tk.Frame(settings_content, bg='white')
        direction_frame.pack(fill='x', pady=(0, 15))
        
        tk.Radiobutton(direction_frame, text="Left to Right", 
                      variable=self.app.blend_direction, value='horizontal',
                      font=('Segoe UI', 9), bg='white', 
                      fg=self.colors['text_dark'],
                      selectcolor=self.colors['primary'],
                      activebackground='white',
                      cursor='hand2').pack(anchor='w', pady=2)
        
        tk.Radiobutton(direction_frame, text="Top to Bottom", 
                      variable=self.app.blend_direction, value='vertical',
                      font=('Segoe UI', 9), bg='white', 
                      fg=self.colors['text_dark'],
                      selectcolor=self.colors['primary'],
                      activebackground='white',
                      cursor='hand2').pack(anchor='w', pady=2)
        
        tk.Radiobutton(direction_frame, text="Diagonal", 
                      variable=self.app.blend_direction, value='diagonal',
                      font=('Segoe UI', 9), bg='white', 
                      fg=self.colors['text_dark'],
                      selectcolor=self.colors['primary'],
                      activebackground='white',
                      cursor='hand2').pack(anchor='w', pady=2)
        
        # Blend strength
        blend_frame = tk.Frame(settings_content, bg='white')
        blend_frame.pack(fill='x', pady=(0, 12))
        
        blend_label_frame = tk.Frame(blend_frame, bg='white')
        blend_label_frame.pack(fill='x')
        
        tk.Label(blend_label_frame, text="Blend Strength:", 
                font=('Segoe UI', 9), bg='white',
                fg=self.colors['text_dark']).pack(side='left')
        
        self.app.blend_alpha_label = tk.Label(blend_label_frame, text="0.50",
                                              font=('Segoe UI', 9, 'bold'),
                                              bg='white', fg=self.colors['primary'])
        self.app.blend_alpha_label.pack(side='right')
        
        self.app.blend_alpha_scale = tk.Scale(blend_frame, from_=0.0, to=1.0,
                                             resolution=0.01,
                                             variable=self.app.blend_alpha,
                                             orient='horizontal',
                                             bg='white', fg=self.colors['primary'],
                                             troughcolor=self.colors['secondary'],
                                             highlightthickness=0,
                                             showvalue=False,
                                             command=self.app.update_blend_alpha_label)
        self.app.blend_alpha_scale.pack(fill='x', pady=(5, 0))
        
        # Apply button
        button_frame = tk.Frame(left_panel, bg='white')
        button_frame.pack(fill='x', pady=15, padx=15)
        
        tk.Button(button_frame, text="Blend Images", 
                 command=self.app.blend_images,
                 bg=self.colors['success'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=20, pady=12, cursor='hand2',
                 activebackground='#229954').pack(fill='x')
        
        # === PREVIEW ===
        preview_header = tk.Frame(right_panel, bg=self.colors['primary'], height=45)
        preview_header.pack(fill='x')
        preview_header.pack_propagate(False)
        
        tk.Label(preview_header, text="Preview", 
                font=('Segoe UI', 11, 'bold'), fg='white', 
                bg=self.colors['primary']).pack(pady=12, padx=15, anchor='w')
        
        preview_content = tk.Frame(right_panel, bg='white')
        preview_content.pack(fill='both', expand=True)
        
        preview_grid = tk.Frame(preview_content, bg='white')
        preview_grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        preview_grid.columnconfigure(0, weight=1)
        preview_grid.columnconfigure(1, weight=1)
        preview_grid.columnconfigure(2, weight=1)
        preview_grid.rowconfigure(0, weight=1)
        
        # Image 1
        img1_frame = self._create_preview_box(preview_grid, "Image 1")
        img1_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        self.app.blend_img1_canvas = tk.Canvas(img1_frame, 
                                               bg=self.colors['secondary'],
                                               highlightthickness=0)
        self.app.blend_img1_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Image 2
        img2_frame = self._create_preview_box(preview_grid, "Image 2")
        img2_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        self.app.blend_img2_canvas = tk.Canvas(img2_frame, 
                                               bg=self.colors['secondary'],
                                               highlightthickness=0)
        self.app.blend_img2_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Result
        result_frame = self._create_preview_box(preview_grid, "Blended Result")
        result_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        
        self.app.blend_result_canvas = tk.Canvas(result_frame, 
                                                 bg=self.colors['secondary'],
                                                 highlightthickness=0)
        self.app.blend_result_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status
        status_frame = tk.Frame(preview_content, bg='white', height=40)
        status_frame.pack(fill='x', padx=10)
        status_frame.pack_propagate(False)
        
        self.app.blending_status = tk.Label(status_frame, text="Ready to blend",
                                           font=('Segoe UI', 9), 
                                           fg=self.colors['text_light'],
                                           bg='white')
        self.app.blending_status.pack(pady=10)
    
    def create_extraction_tab(self):
        extraction_frame = tk.Frame(self.notebook, bg=self.colors['secondary'])
        self.notebook.add(extraction_frame, text="  Extraction  ")
        
        main_container = tk.Frame(extraction_frame, bg=self.colors['secondary'])
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Left panel
        left_panel = tk.Frame(main_container, bg=self.colors['white'], relief='flat', bd=1)
        left_panel.pack(side='left', fill='both', padx=(0, 10))
        left_panel.configure(width=350)
        
        # Right panel
        right_panel = tk.Frame(main_container, bg=self.colors['white'], relief='flat', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # === CONTROLS ===
        selection_section = self._create_control_section(left_panel, "Image Selection")
        
        # Original image
        orig_frame = tk.Frame(selection_section, bg='white')
        orig_frame.pack(fill='x', pady=8, padx=15)
        
        tk.Label(orig_frame, text="Original Image:", 
                font=('Segoe UI', 9), bg='white',
                fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        
        tk.Button(orig_frame, text="Select Original Image", 
                 command=self.app.select_original_image,
                 bg=self.colors['primary'], fg='white',
                 font=('Segoe UI', 9, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2',
                 activebackground=self.colors['hover']).pack(fill='x')
        
        self.app.original_image_label = tk.Label(orig_frame, text="No image selected",
                                                 font=('Segoe UI', 8), 
                                                 fg=self.colors['text_light'],
                                                 bg='white', anchor='w')
        self.app.original_image_label.pack(fill='x', pady=(5, 0))
        
        # Watermarked image
        water_frame = tk.Frame(selection_section, bg='white')
        water_frame.pack(fill='x', pady=8, padx=15)
        
        tk.Label(water_frame, text="Watermarked Image:", 
                font=('Segoe UI', 9), bg='white',
                fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        
        tk.Button(water_frame, text="Select Watermarked Image", 
                 command=self.app.select_watermarked_image,
                 bg=self.colors['primary'], fg='white',
                 font=('Segoe UI', 9, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2',
                 activebackground=self.colors['hover']).pack(fill='x')
        
        self.app.watermarked_image_label = tk.Label(water_frame, text="No image selected",
                                                    font=('Segoe UI', 8), 
                                                    fg=self.colors['text_light'],
                                                    bg='white', anchor='w')
        self.app.watermarked_image_label.pack(fill='x', pady=(5, 0))
        
        # Method
        method_section = self._create_control_section(left_panel, "Extraction Method")
        
        method_content = tk.Frame(method_section, bg='white')
        method_content.pack(fill='x', pady=8, padx=15)
        
        tk.Radiobutton(method_content, text="Fourier Transform", 
                      variable=self.app.extraction_method, value='fourier',
                      font=('Segoe UI', 9), bg='white', 
                      fg=self.colors['text_dark'],
                      selectcolor=self.colors['primary'],
                      activebackground='white',
                      cursor='hand2').pack(anchor='w', pady=2)
        
        tk.Radiobutton(method_content, text="Edge Detection", 
                      variable=self.app.extraction_method, value='edge',
                      font=('Segoe UI', 9), bg='white', 
                      fg=self.colors['text_dark'],
                      selectcolor=self.colors['primary'],
                      activebackground='white',
                      cursor='hand2').pack(anchor='w', pady=2)
        
        # Extract button
        button_frame = tk.Frame(left_panel, bg='white')
        button_frame.pack(fill='x', pady=15, padx=15)
        
        tk.Button(button_frame, text="Extract Watermark", 
                 command=self.app.extract_watermark,
                 bg=self.colors['success'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=20, pady=12, cursor='hand2',
                 activebackground='#229954').pack(fill='x')
        
        # === PREVIEW ===
        preview_header = tk.Frame(right_panel, bg=self.colors['primary'], height=45)
        preview_header.pack(fill='x')
        preview_header.pack_propagate(False)
        
        tk.Label(preview_header, text="Preview", 
                font=('Segoe UI', 11, 'bold'), fg='white', 
                bg=self.colors['primary']).pack(pady=12, padx=15, anchor='w')
        
        preview_content = tk.Frame(right_panel, bg='white')
        preview_content.pack(fill='both', expand=True)
        
        preview_grid = tk.Frame(preview_content, bg='white')
        preview_grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        preview_grid.columnconfigure(0, weight=1)
        preview_grid.columnconfigure(1, weight=1)
        preview_grid.columnconfigure(2, weight=1)
        preview_grid.rowconfigure(0, weight=1)
        
        # Original
        orig_preview_frame = self._create_preview_box(preview_grid, "Original")
        orig_preview_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        self.app.extract_orig_canvas = tk.Canvas(orig_preview_frame, 
                                                 bg=self.colors['secondary'],
                                                 highlightthickness=0)
        self.app.extract_orig_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Watermarked
        water_preview_frame = self._create_preview_box(preview_grid, "Watermarked")
        water_preview_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        self.app.extract_water_canvas = tk.Canvas(water_preview_frame, 
                                                  bg=self.colors['secondary'],
                                                  highlightthickness=0)
        self.app.extract_water_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Extracted
        result_preview_frame = self._create_preview_box(preview_grid, "Extracted")
        result_preview_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        
        self.app.extract_result_canvas = tk.Canvas(result_preview_frame, 
                                                   bg=self.colors['secondary'],
                                                   highlightthickness=0)
        self.app.extract_result_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status
        status_frame = tk.Frame(preview_content, bg='white', height=40)
        status_frame.pack(fill='x', padx=10)
        status_frame.pack_propagate(False)
        
        self.app.extraction_status = tk.Label(status_frame, text="Ready to extract",
                                             font=('Segoe UI', 9), 
                                             fg=self.colors['text_light'],
                                             bg='white')
        self.app.extraction_status.pack(pady=10)
    
    def create_results_tab(self):
        results_frame = tk.Frame(self.notebook, bg=self.colors['secondary'])
        self.notebook.add(results_frame, text="  Results  ")
        
        content = tk.Frame(results_frame, bg=self.colors['white'], relief='flat', bd=1)
        content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header
        header = tk.Frame(content, bg=self.colors['primary'], height=45)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="Operation Results", 
                font=('Segoe UI', 11, 'bold'), fg='white', 
                bg=self.colors['primary']).pack(pady=12, padx=15, anchor='w')
        
        # Results text
        text_frame = tk.Frame(content, bg='white')
        text_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.app.results_text = scrolledtext.ScrolledText(text_frame, 
                                                          height=20,
                                                          font=('Consolas', 9),
                                                          bg=self.colors['secondary'],
                                                          fg=self.colors['text_dark'],
                                                          relief='flat',
                                                          borderwidth=5)
        self.app.results_text.pack(fill='both', expand=True)
        
        # Clear button
        tk.Button(text_frame, text="Clear Results", 
                 command=self.app.clear_results,
                 bg=self.colors['danger'], fg='white',
                 font=('Segoe UI', 9, 'bold'), relief='flat',
                 padx=15, pady=8, cursor='hand2').pack(pady=(10, 0))
    
    def _create_control_section(self, parent, title):
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', pady=(0, 1))
        
        title_bar = tk.Frame(frame, bg=self.colors['secondary'], height=35)
        title_bar.pack(fill='x')
        title_bar.pack_propagate(False)
        
        tk.Label(title_bar, text=title, 
                font=('Segoe UI', 9, 'bold'),
                bg=self.colors['secondary'], 
                fg=self.colors['text_dark'],
                anchor='w').pack(fill='x', padx=15, pady=8)
        
        return frame
    
    def _create_preview_box(self, parent, title):
        frame = tk.Frame(parent, bg='white', relief='solid', bd=1,
                        highlightbackground=self.colors['border'],
                        highlightthickness=1)
        
        title_label = tk.Label(frame, text=title, 
                              font=('Segoe UI', 9, 'bold'),
                              bg=self.colors['secondary'], 
                              fg=self.colors['text_dark'])
        title_label.pack(fill='x', pady=5)
        
        return frame
    
    def display_image_preview(self, canvas, image_path, max_width=300, max_height=250):
        try:
            img = Image.open(image_path)
            
            img_width, img_height = img.size
            scale = min(max_width / img_width, max_height / img_height, 1.0)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_resized)
            
            canvas.image = photo
            
            canvas.delete("all")
            canvas_width = canvas.winfo_width() if canvas.winfo_width() > 1 else max_width
            canvas_height = canvas.winfo_height() if canvas.winfo_height() > 1 else max_height
            
            canvas.create_image(canvas_width // 2, canvas_height // 2, 
                              image=photo, anchor='center')
            
            return True
        except Exception as e:
            canvas.delete("all")
            canvas.create_text(150, 125,
                             text=f"Unable to load image",
                             fill=self.colors['text_light'], 
                             font=('Segoe UI', 9))
            return False