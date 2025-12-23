import tkinter as tk
from tkinter import messagebox, ttk, filedialog, colorchooser
import random
import copy
import time

# ------------------- Default Color Theme -------------------
COLORS = {
    'primary': '#2563eb',      
    'primary_hover': '#1d4ed8', 
    'primary_dark': '#1e40af',  
    'secondary': '#7c3aed',     
    'success': '#059669',       
    'success_light': '#d1fae5', 
    'warning': '#d97706',       
    'warning_light': '#fef3c7', 
    'error': '#dc2626',         
    'error_light': '#fef2f2',   
    'gray_50': '#f9fafb',
    'gray_100': '#f3f4f6',
    'gray_200': '#e5e7eb',
    'gray_300': '#d1d5db',
    'gray_400': '#9ca3af',
    'gray_500': '#6b7280',
    'gray_600': '#4b5563',
    'gray_700': '#374151',
    'gray_800': '#1f2937',
    'gray_900': '#111827',
    'white': '#ffffff',
    'black': '#000000',
    'blue_light': '#dbeafe',    
    'cyan_light': '#cffafe',    
    'correct': '#bbf7d0',
    'board_bg': '#f0f9ff',
    'hint_bg': '#fef3c7'
}

# ------------------- Smart Sudoku Solver -------------------

class SmartSudokuSolver:
    """Advanced Sudoku solver with comprehensive validation"""
    
    @staticmethod
    def is_valid_move(board, row, col, num):
        """Check if placing num at (row, col) is valid according to Sudoku rules"""
        for j in range(9):
            if j != col and board[row][j] == num:
                return False
        
        for i in range(9):
            if i != row and board[i][col] == num:
                return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i != row or j != col) and board[i][j] == num:
                    return False
        
        return True
    
    @staticmethod
    def find_empty(board):
        """Find next empty cell (0)"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    @staticmethod
    def solve(board):
        """Solve sudoku using backtracking algorithm"""
        empty = SmartSudokuSolver.find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        for num in range(1, 10):
            if SmartSudokuSolver.is_valid_move(board, row, col, num):
                board[row][col] = num
                if SmartSudokuSolver.solve(board):
                    return True
                board[row][col] = 0
        
        return False
    
    @staticmethod
    def is_valid_puzzle(board):
        """Check if current puzzle state is valid (no conflicts)"""
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    num = board[i][j]
                    board[i][j] = 0
                    valid = SmartSudokuSolver.is_valid_move(board, i, j, num)
                    board[i][j] = num
                    if not valid:
                        return False
        return True
    
    @staticmethod
    def count_solutions(board, limit=2):
        """Count number of solutions (up to limit)"""
        solutions = []
        SmartSudokuSolver._find_all_solutions(copy.deepcopy(board), solutions, limit)
        return len(solutions)
    
    @staticmethod
    def _find_all_solutions(board, solutions, max_solutions):
        """Find all solutions up to max_solutions"""
        if len(solutions) >= max_solutions:
            return
        
        empty = SmartSudokuSolver.find_empty(board)
        if not empty:
            solutions.append(copy.deepcopy(board))
            return
        
        row, col = empty
        for num in range(1, 10):
            if SmartSudokuSolver.is_valid_move(board, row, col, num):
                board[row][col] = num
                SmartSudokuSolver._find_all_solutions(board, solutions, max_solutions)
                board[row][col] = 0

# ------------------- Puzzle Generator -------------------

def generate_puzzle(difficulty="medium"):
    """Generate a valid sudoku puzzle with unique solution"""
    difficulty_levels = {
        "easy": 40,
        "medium": 32,   
        "hard": 26,     
        "expert": 22
    }
    
    clues = difficulty_levels.get(difficulty, 32)
    
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    for box in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        idx = 0
        for i in range(3):
            for j in range(3):
                board[box + i][box + j] = nums[idx]
                idx += 1
    
    SmartSudokuSolver.solve(board)
    solution = copy.deepcopy(board)
    
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    
    removed = 0
    target_removed = 81 - clues
    
    for i, j in cells:
        if removed >= target_removed:
            break
            
        backup = board[i][j]
        board[i][j] = 0
        
        if SmartSudokuSolver.count_solutions(board, 2) == 1:
            removed += 1
        else:
            board[i][j] = backup
    
    return board, solution

# ------------------- Modern Button Class -------------------

class ModernButton(tk.Button):
    def __init__(self, parent, **kwargs):
        bg_color = kwargs.pop('bg_color', COLORS['primary'])
        hover_color = kwargs.pop('hover_color', COLORS['primary_hover'])
        active_color = kwargs.pop('active_color', COLORS['primary_dark'])
        
        default_style = {
            'font': ('Segoe UI', 10, 'bold'),
            'bg': bg_color,
            'fg': COLORS['white'],
            'bd': 0,
            'relief': 'flat',
            'cursor': 'hand2',
            'pady': 8,
            'padx': 15,
            'activebackground': active_color,
            'activeforeground': COLORS['white']
        }
        
        default_style.update(kwargs)
        super().__init__(parent, **default_style)
        
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.active_color = active_color
        
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_color))
        self.bind("<Leave>", lambda e: self.config(bg=self.bg_color))

# ------------------- Main Sudoku Game -------------------

class SudokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("🎯 Sudoku Master - Enhanced Edition")
        self.master.state('zoomed')
        try:
            self.master.attributes('-zoomed', True)
        except:
            pass
        self.master.resizable(True, True)
        
        # Theme colors
        self.bg_color = COLORS['white']
        self.button_color = COLORS['primary']
        
        self.master.configure(bg=self.bg_color)
        
        # Game settings
        self.auto_check = tk.BooleanVar(value=True)
        self.timer_mode = tk.StringVar(value="count_up")
        self.countdown_minutes = tk.IntVar(value=15)
        
        # Game state
        self.difficulty = "medium"
        self.puzzle, self.solution = generate_puzzle(self.difficulty)
        self.original_puzzle = copy.deepcopy(self.puzzle)
        self.user_puzzle = copy.deepcopy(self.puzzle)
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.selected_cell = None
        self.game_completed = False
        self.hints_used = 0
        self.timer_seconds = 0
        self.timer_running = False
        self.start_time = time.time()
        
        # Store button references for theme updates
        self.buttons = []
        
        # Create UI
        self.create_ui()
        self.start_timer()

    def create_ui(self):
        """Create the complete UI with scrolling"""
        self.main_canvas = tk.Canvas(self.master, bg=self.bg_color)
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg=self.bg_color)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.main_canvas.unbind_all("<MouseWheel>")
        
        self.main_canvas.bind('<Enter>', _bind_to_mousewheel)
        self.main_canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        self.create_header()
        self.create_game_board()
        self.create_control_panel()
        self.create_footer()

    def create_header(self):
        """Create header with title and stats"""
        header_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color, pady=20)
        header_frame.pack(fill="x")
        
        title_frame = tk.Frame(header_frame, bg=self.button_color, relief='raised', bd=2)
        title_frame.pack(pady=(0, 15))
        
        title_label = tk.Label(
            title_frame,
            text="🎯 SUDOKU MASTER",
            font=('Segoe UI', 28, 'bold'),
            fg=COLORS['white'],
            bg=self.button_color,
            pady=15
        )
        title_label.pack()
        
        stats_frame = tk.Frame(header_frame, bg=COLORS['gray_100'], relief='raised', bd=1)
        stats_frame.pack(fill="x", padx=20)
        
        stats_inner = tk.Frame(stats_frame, bg=COLORS['gray_100'])
        stats_inner.pack(pady=10)
        
        self.timer_label = tk.Label(
            stats_inner,
            text="⏱ 00:00",
            font=('Segoe UI', 16, 'bold'),
            fg=self.button_color,
            bg=COLORS['gray_100']
        )
        self.timer_label.pack(side="left", padx=30)
        
        self.difficulty_label = tk.Label(
            stats_inner,
            text=f"📊 Level: {self.difficulty.title()}",
            font=('Segoe UI', 14, 'bold'),
            fg=COLORS['gray_700'],
            bg=COLORS['gray_100']
        )
        self.difficulty_label.pack(side="left", padx=30)
        
        self.hints_label = tk.Label(
            stats_inner,
            text=f"💡 Hints: {self.hints_used}",
            font=('Segoe UI', 14, 'bold'),
            fg=COLORS['gray_700'],
            bg=COLORS['gray_100']
        )
        self.hints_label.pack(side="left", padx=30)

    def create_game_board(self):
        """Create the sudoku grid"""
        board_container = tk.Frame(self.scrollable_frame, bg=COLORS['gray_800'], relief='raised', bd=3)
        board_container.pack(pady=30)
        
        board_frame = tk.Frame(board_container, bg=COLORS['gray_800'], padx=6, pady=6)
        board_frame.pack()
        
        for i in range(9):
            for j in range(9):
                padx = (3, 3)
                pady = (3, 3)
                
                if j % 3 == 2 and j != 8:
                    padx = (3, 8)
                if i % 3 == 2 and i != 8:
                    pady = (3, 8)
                
                entry = tk.Entry(
                    board_frame,
                    width=4,
                    font=('Segoe UI', 24, 'bold'),
                    justify="center",
                    bd=3,
                    relief='solid',
                    highlightthickness=4,
                    highlightcolor=self.button_color,
                    highlightbackground=COLORS['gray_300']
                )
                
                entry.grid(row=i, column=j, padx=padx, pady=pady, ipady=12)
                
                value = self.puzzle[i][j]
                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(
                        state="readonly",
                        readonlybackground=COLORS['gray_200'],
                        fg=COLORS['gray_900'],
                        font=('Segoe UI', 24, 'bold')
                    )
                else:
                    entry.config(
                        bg=COLORS['white'], 
                        fg=self.button_color,
                        insertbackground=self.button_color
                    )
                    entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.on_cell_change(r, c))
                    entry.bind('<FocusIn>', lambda e, r=i, c=j: self.on_focus_in(r, c))
                    entry.bind('<FocusOut>', lambda e, r=i, c=j: self.on_focus_out(r, c))
                
                self.cells[i][j] = entry

    def create_control_panel(self):
        """Create control buttons and settings"""
        control_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        control_frame.pack(pady=20, fill="x", padx=20)
        
        # Game Control Buttons
        button_frame1 = tk.Frame(control_frame, bg=self.bg_color)
        button_frame1.pack(pady=5)
        
        btn1 = ModernButton(
            button_frame1,
            text="🆕 New Game",
            command=self.new_game,
            bg_color=COLORS['success'],
            hover_color='#047857',
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn1.pack(side="left", padx=8)
        self.buttons.append(btn1)
        
        btn2 = ModernButton(
            button_frame1,
            text="✅ Check Solution",
            command=self.check_solution,
            bg_color=self.button_color,
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn2.pack(side="left", padx=8)
        self.buttons.append(btn2)
        
        btn3 = ModernButton(
            button_frame1,
            text="🔍 Show Solution",
            command=self.show_solution,
            bg_color=COLORS['secondary'],
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn3.pack(side="left", padx=8)
        self.buttons.append(btn3)
        
        btn4 = ModernButton(
            button_frame1,
            text="💡 Get Hint",
            command=self.give_hint,
            bg_color=COLORS['warning'],
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn4.pack(side="left", padx=8)
        self.buttons.append(btn4)
        
        # File and Utility Buttons
        button_frame2 = tk.Frame(control_frame, bg=self.bg_color)
        button_frame2.pack(pady=5)
        
        btn5 = ModernButton(
            button_frame2,
            text="📁 Upload Puzzle",
            command=self.load_from_file,
            bg_color=COLORS['primary_dark'],
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn5.pack(side="left", padx=8)
        self.buttons.append(btn5)
        
        btn6 = ModernButton(
            button_frame2,
            text="💾 Save Puzzle",
            command=self.save_to_file,
            bg_color=COLORS['primary_dark'],
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn6.pack(side="left", padx=8)
        self.buttons.append(btn6)
        
        btn7 = ModernButton(
            button_frame2,
            text="📥 Download Solution",
            command=self.download_solution,
            bg_color=COLORS['success'],
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn7.pack(side="left", padx=8)
        self.buttons.append(btn7)
        
        btn8 = ModernButton(
            button_frame2,
            text="🗑 Clear Board",
            command=self.clear_board,
            bg_color=COLORS['gray_600'],
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn8.pack(side="left", padx=8)
        self.buttons.append(btn8)
        
        # Theme Buttons
        button_frame3 = tk.Frame(control_frame, bg=self.bg_color)
        button_frame3.pack(pady=5)
        
        btn9 = ModernButton(
            button_frame3,
            text="🎨 Change Background",
            command=self.change_bg_color,
            bg_color=COLORS['secondary'],
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn9.pack(side="left", padx=8)
        self.buttons.append(btn9)
        
        btn10 = ModernButton(
            button_frame3,
            text="🖌 Change Buttons",
            command=self.change_button_color,
            bg_color=COLORS['secondary'],
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn10.pack(side="left", padx=8)
        self.buttons.append(btn10)
        
        btn11 = ModernButton(
            button_frame3,
            text="❓ Help",
            command=self.show_help,
            bg_color=COLORS['gray_500'],
            font=('Segoe UI', 12, 'bold'),
            pady=10,
            padx=20
        )
        btn11.pack(side="left", padx=8)
        self.buttons.append(btn11)
        
        # Settings Section
        settings_frame = tk.LabelFrame(
            control_frame, 
            text="⚙️ Game Settings", 
            bg=COLORS['gray_100'],
            fg=COLORS['gray_800'],
            font=('Segoe UI', 12, 'bold'),
            pady=10
        )
        settings_frame.pack(pady=15, fill="x")
        
        settings_inner = tk.Frame(settings_frame, bg=COLORS['gray_100'])
        settings_inner.pack(fill="x", padx=10)
        
        # Auto-check setting
        check_frame = tk.Frame(settings_inner, bg=COLORS['gray_100'])
        check_frame.pack(side="left", padx=15, fill="y")
        
        tk.Checkbutton(
            check_frame,
            text="🔍 Auto-check entries",
            variable=self.auto_check,
            command=self.toggle_auto_check,
            font=('Segoe UI', 11),
            bg=COLORS['gray_100'],
            activebackground=COLORS['gray_100'],
            fg=COLORS['gray_800']
        ).pack(anchor="w")
        
        # Timer mode setting
        timer_frame = tk.Frame(settings_inner, bg=COLORS['gray_100'])
        timer_frame.pack(side="left", padx=20, fill="y")
        
        tk.Label(
            timer_frame,
            text="⏱ Timer Mode:",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['gray_100'],
            fg=COLORS['gray_800']
        ).pack(anchor="w")
        
        timer_modes = [("Count Up ⬆", "count_up"), ("Count Down ⬇", "count_down"), ("Free Play ∞", "free")]
        for text, mode in timer_modes:
            tk.Radiobutton(
                timer_frame,
                text=text,
                variable=self.timer_mode,
                value=mode,
                command=self.reset_timer,
                font=('Segoe UI', 10),
                bg=COLORS['gray_100'],
                activebackground=COLORS['gray_100'],
                fg=COLORS['gray_700']
            ).pack(anchor="w")
        
        # Custom countdown time
        countdown_frame = tk.Frame(settings_inner, bg=COLORS['gray_100'])
        countdown_frame.pack(side="left", padx=20, fill="y")
        
        tk.Label(
            countdown_frame,
            text="⏰ Countdown Minutes:",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['gray_100'],
            fg=COLORS['gray_800']
        ).pack(anchor="w")
        
        timer_spinbox = tk.Spinbox(
            countdown_frame,
            from_=1,
            to=60,
            textvariable=self.countdown_minutes,
            width=10,
            font=('Segoe UI', 10),
            command=self.update_countdown_time
        )
        timer_spinbox.pack(anchor="w", pady=5)
        
        # Difficulty Selection
        diff_frame = tk.Frame(control_frame, bg=self.bg_color)
        diff_frame.pack(pady=10)
        
        tk.Label(
            diff_frame,
            text="🎚 Difficulty Level:",
            font=('Segoe UI', 12, 'bold'),
            bg=self.bg_color,
            fg=COLORS['gray_800']
        ).pack()
        
        diff_buttons = tk.Frame(diff_frame, bg=self.bg_color)
        diff_buttons.pack(pady=5)
        
        difficulty_info = {
            "easy": ("😊 Easy", COLORS['success']),
            "medium": ("🙂 Medium", COLORS['warning']),
            "hard": ("😤 Hard", COLORS['error']),
            "expert": ("🤯 Expert", COLORS['gray_800'])
        }
        
        self.diff_buttons_refs = {}
        for diff, (text, color) in difficulty_info.items():
            bg_color = color if diff == self.difficulty else COLORS['gray_400']
            btn = ModernButton(
                diff_buttons,
                text=text,
                command=lambda d=diff: self.change_difficulty(d),
                bg_color=bg_color,
                font=('Segoe UI', 10, 'bold'),
                pady=6,
                padx=12
            )
            btn.pack(side="left", padx=3)
            self.diff_buttons_refs[diff] = (btn, color)

    def create_footer(self):
        """Create footer"""
        footer_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        footer_frame.pack(fill="x", pady=20)
        
        info_frame = tk.LabelFrame(
            footer_frame,
            text="📋 File Format Instructions",
            bg=COLORS['blue_light'],
            fg=COLORS['primary_dark'],
            font=('Segoe UI', 11, 'bold')
        )
        info_frame.pack(fill="x", padx=20, pady=10)
        
        instruction_text = (
            "📁 How to create a puzzle file (.txt):\n"
            "• Create a text file with exactly 81 digits (9x9 = 81)\n"
            "• Use digits 1-9 for filled cells, use 0 for empty cells\n"
            "• Arrange digits row by row: first 9 digits = row 1, next 9 = row 2, etc.\n"
            "• Example: 530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        )
        
        tk.Label(
            info_frame,
            text=instruction_text,
            font=('Segoe UI', 10),
            fg=COLORS['primary_dark'],
            bg=COLORS['blue_light'],
            justify="left"
        ).pack(pady=10, padx=15)
        
        credits_frame = tk.Frame(footer_frame, bg=self.button_color, relief='raised', bd=3)
        credits_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            credits_frame,
            text="✨ Crafted with Precision & Passion ✨",
            font=('Segoe UI', 12, 'bold'),
            fg=COLORS['white'],
            bg=self.button_color
        ).pack(pady=(15, 5))
        
        tk.Label(
            credits_frame,
            text="👨‍💻 MUTAIB • ANDRIE • FAWAD 👨‍💻",
            font=('Segoe UI', 16, 'bold'),
            fg=COLORS['white'],
            bg=self.button_color
        ).pack(pady=5)
        
        tk.Label(
            credits_frame,
            text="🏛 Universitas Syiah Kuala © 2025 🏛",
            font=('Segoe UI', 12),
            fg=COLORS['gray_200'],
            bg=self.button_color
        ).pack(pady=(5, 15))

    def toggle_auto_check(self):
        """Toggle auto-check and update cells"""
        if not self.auto_check.get():
            # Clear all color coding when turned off
            for i in range(9):
                for j in range(9):
                    if self.cells[i][j]['state'] != 'readonly':
                        self.cells[i][j].config(bg=COLORS['white'])
        else:
            # Revalidate all cells when turned on
            for i in range(9):
                for j in range(9):
                    if self.cells[i][j]['state'] != 'readonly':
                        val = self.cells[i][j].get()
                        if val and val.isdigit():
                            self.validate_cell(i, j, int(val))

    def update_countdown_time(self):
        """Update countdown time when spinbox changes"""
        if self.timer_mode.get() == "count_down":
            self.reset_timer()

    def change_bg_color(self):
        """Change background color theme"""
        color = colorchooser.askcolor(title="Choose Background Color", initialcolor=self.bg_color)
        if color[1]:
            self.bg_color = color[1]
            self.apply_bg_theme()

    def change_button_color(self):
        """Change button color theme"""
        color = colorchooser.askcolor(title="Choose Button Color", initialcolor=self.button_color)
        if color[1]:
            self.button_color = color[1]
            self.apply_button_theme()

    def apply_bg_theme(self):
        """Apply background color to all frames"""
        self.master.configure(bg=self.bg_color)
        self.main_canvas.configure(bg=self.bg_color)
        self.scrollable_frame.configure(bg=self.bg_color)
        
        # Update all frames recursively
        for widget in self.scrollable_frame.winfo_children():
            self.update_widget_bg(widget)

    def update_widget_bg(self, widget):
        """Recursively update widget backgrounds"""
        try:
            if isinstance(widget, (tk.Frame,)) and widget.cget('bg') not in [COLORS['gray_100'], COLORS['blue_light'], COLORS['gray_800']]:
                widget.configure(bg=self.bg_color)
            if isinstance(widget, tk.Label) and widget.cget('bg') == COLORS['white']:
                widget.configure(bg=self.bg_color)
        except:
            pass
        
        for child in widget.winfo_children():
            self.update_widget_bg(child)

    def apply_button_theme(self):
        """Apply button color theme"""
        # Update timer label color
        self.timer_label.configure(fg=self.button_color)
        
        # Update cell highlight colors
        for i in range(9):
            for j in range(9):
                if self.cells[i][j]['state'] != 'readonly':
                    self.cells[i][j].configure(
                        fg=self.button_color,
                        insertbackground=self.button_color,
                        highlightcolor=self.button_color
                    )
        
        # Update difficulty buttons to maintain proper colors
        difficulty_info = {
            "easy": COLORS['success'],
            "medium": COLORS['warning'],
            "hard": COLORS['error'],
            "expert": COLORS['gray_800']
        }
        
        for diff, (btn, orig_color) in self.diff_buttons_refs.items():
            if diff == self.difficulty:
                btn.config(bg=orig_color)
                btn.bg_color = orig_color
            else:
                btn.config(bg=COLORS['gray_400'])
                btn.bg_color = COLORS['gray_400']

    def download_solution(self):
        """Download the solved puzzle as .txt file"""
        if not self.is_puzzle_complete():
            if not messagebox.askyesno(
                "⚠️ Puzzle Incomplete",
                "The puzzle is not completely solved yet.\n\n"
                "Do you want to download the complete solution instead?"
            ):
                return
            
            # Use the solution
            save_puzzle = self.solution
            title = "Complete Solution"
        else:
            # Use current state
            save_puzzle = self.user_puzzle
            title = "Solved Puzzle"
        
        file_path = filedialog.asksaveasfilename(
            title=f"💾 Download {title}",
            defaultextension=".txt",
            initialfile=f"sudoku_solution_{int(time.time())}.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w') as file:
                # Write title
                file.write(f"# SUDOKU {title.upper()}\n")
                file.write(f"# Difficulty: {self.difficulty.title()}\n")
                file.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("#" + "="*50 + "\n\n")
                
                # Write compact format (81 digits)
                puzzle_string = ""
                for i in range(9):
                    for j in range(9):
                        puzzle_string += str(save_puzzle[i][j])
                
                file.write("# Compact format (81 digits):\n")
                file.write(puzzle_string + "\n\n")
                
                # Write formatted view
                file.write("# Formatted view:\n")
                file.write("# ┌───────┬───────┬───────┐\n")
                for i in range(9):
                    row = "# │ "
                    for j in range(9):
                        row += str(save_puzzle[i][j]) + " "
                        if j % 3 == 2:
                            row += "│ "
                    file.write(row + "\n")
                    
                    if i % 3 == 2 and i != 8:
                        file.write("# ├───────┼───────┼───────┤\n")
                
                file.write("# └───────┴───────┴───────┘\n")
                
                # Add statistics
                if self.is_puzzle_complete():
                    file.write(f"\n# Time taken: {self.timer_label.cget('text').replace('⏱ ', '')}\n")
                    file.write(f"# Hints used: {self.hints_used}\n")
            
            messagebox.showinfo(
                "✅ Download Successful",
                f"Solution saved successfully!\n\n"
                f"📁 File: {file_path}"
            )
            
        except Exception as e:
            messagebox.showerror("❌ Download Error", f"Failed to save solution:\n{str(e)}")

    def on_cell_change(self, row, col):
        """Handle cell value changes with intelligent validation"""
        entry = self.cells[row][col]
        val = entry.get()
        
        if val == "":
            self.user_puzzle[row][col] = 0
            entry.config(bg=COLORS['white'])
            return
        
        if not val.isdigit() or val == "0" or len(val) > 1:
            entry.delete(0, tk.END)
            if self.user_puzzle[row][col] != 0:
                entry.insert(0, str(self.user_puzzle[row][col]))
            return
        
        num = int(val)
        self.user_puzzle[row][col] = num
        
        if self.auto_check.get():
            self.validate_cell(row, col, num)
        else:
            entry.config(bg=COLORS['white'])
        
        if self.is_puzzle_complete():
            self.on_puzzle_complete()

    def validate_cell(self, row, col, num):
        """Validate a single cell and apply appropriate color coding"""
        entry = self.cells[row][col]
        
        if num == self.solution[row][col]:
            entry.config(bg=COLORS['correct'], fg=COLORS['gray_900'])
            return
        
        temp_val = self.user_puzzle[row][col]
        self.user_puzzle[row][col] = 0
        
        if SmartSudokuSolver.is_valid_move(self.user_puzzle, row, col, num):
            entry.config(bg=COLORS['warning_light'], fg=COLORS['gray_800'])
        else:
            entry.config(bg=COLORS['error_light'], fg=COLORS['error'])
        
        self.user_puzzle[row][col] = temp_val

    def on_focus_in(self, row, col):
        """Handle cell focus with visual feedback"""
        self.selected_cell = (row, col)
        self.highlight_related_cells(row, col)

    def on_focus_out(self, row, col):
        """Handle cell focus out"""
        if self.auto_check.get():
            val = self.cells[row][col].get()
            if val and val.isdigit():
                self.validate_cell(row, col, int(val))
        self.clear_highlights()

    def highlight_related_cells(self, row, col):
        """Highlight related cells"""
        for i in range(9):
            for j in range(9):
                if self.cells[i][j]['state'] != 'readonly':
                    if i == row or j == col or (i//3 == row//3 and j//3 == col//3):
                        if (i, j) != (row, col):
                            current_bg = self.cells[i][j]['bg']
                            if current_bg == COLORS['white']:
                                self.cells[i][j].config(bg=COLORS['gray_100'])

    def clear_highlights(self):
        """Clear cell highlights"""
        for i in range(9):
            for j in range(9):
                if self.cells[i][j]['state'] != 'readonly':
                    val = self.cells[i][j].get()
                    if val and val.isdigit() and self.auto_check.get():
                        self.validate_cell(i, j, int(val))
                    else:
                        self.cells[i][j].config(bg=COLORS['white'])

    def is_puzzle_complete(self):
        """Check if puzzle is completely and correctly solved"""
        for i in range(9):
            for j in range(9):
                if self.user_puzzle[i][j] != self.solution[i][j]:
                    return False
        return True

    def on_puzzle_complete(self):
        """Handle puzzle completion with animation"""
        if self.game_completed:
            return
            
        self.game_completed = True
        self.timer_running = False
        
        # Create celebration window with animation
        celebration_window = tk.Toplevel(self.master)
        celebration_window.title("🎉 Congratulations!")
        celebration_window.geometry("500x400")
        celebration_window.configure(bg=COLORS['success'])
        celebration_window.resizable(False, False)
        celebration_window.transient(self.master)
        celebration_window.grab_set()
        
        # Center window
        celebration_window.update_idletasks()
        x = (celebration_window.winfo_screenwidth() // 2) - 250
        y = (celebration_window.winfo_screenheight() // 2) - 200
        celebration_window.geometry(f"500x400+{x}+{y}")
        
        # Animated congratulations text
        congrats_label = tk.Label(
            celebration_window,
            text="🎉 CONGRATULATIONS! 🎉",
            font=('Segoe UI', 24, 'bold'),
            fg=COLORS['white'],
            bg=COLORS['success']
        )
        congrats_label.pack(pady=30)
        
        # Animate the text
        self.animate_celebration(congrats_label, 0)
        
        # Stats
        time_str = self.timer_label.cget("text").replace("⏱ ", "")
        time_bonus = max(0, 1800 - self.timer_seconds) // 60
        hint_penalty = self.hints_used * 10
        difficulty_multiplier = {"easy": 1, "medium": 1.5, "hard": 2, "expert": 3}
        score = max(0, int((1000 + time_bonus - hint_penalty) * difficulty_multiplier.get(self.difficulty, 1)))
        
        stats_frame = tk.Frame(celebration_window, bg=COLORS['white'], relief='raised', bd=3)
        stats_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        stats_text = f"""
        🏆 PUZZLE SOLVED! 🏆
        
        ⏱ Time: {time_str}
        💡 Hints Used: {self.hints_used}
        📊 Difficulty: {self.difficulty.title()}
        ⭐ Score: {score} points
        
        Outstanding performance!
        Ready for the next challenge?
        """
        
        tk.Label(
            stats_frame,
            text=stats_text,
            font=('Segoe UI', 14),
            fg=COLORS['gray_800'],
            bg=COLORS['white'],
            justify='center'
        ).pack(pady=20)
        
        # Buttons
        btn_frame = tk.Frame(celebration_window, bg=COLORS['success'])
        btn_frame.pack(pady=20)
        
        ModernButton(
            btn_frame,
            text="🆕 New Game",
            command=lambda: [celebration_window.destroy(), self.new_game()],
            bg_color=COLORS['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(side="left", padx=10)
        
        ModernButton(
            btn_frame,
            text="📥 Download Solution",
            command=lambda: [celebration_window.destroy(), self.download_solution()],
            bg_color=COLORS['secondary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(side="left", padx=10)
        
        ModernButton(
            btn_frame,
            text="✅ Close",
            command=celebration_window.destroy,
            bg_color=COLORS['gray_600'],
            font=('Segoe UI', 12, 'bold')
        ).pack(side="left", padx=10)

    def animate_celebration(self, label, step):
        """Animate celebration text"""
        colors = [COLORS['white'], '#FFD700', '#FFA500', '#FF6347', '#FFD700', COLORS['white']]
        if label.winfo_exists():
            label.config(fg=colors[step % len(colors)])
            self.master.after(200, lambda: self.animate_celebration(label, step + 1))

    def check_solution(self):
        """Comprehensive solution validation"""
        conflicts = []
        incorrect = []
        empty_cells = []
        
        validation_board = copy.deepcopy(self.user_puzzle)
        
        for i in range(9):
            for j in range(9):
                val = self.cells[i][j].get()
                
                if not val or val == "0":
                    empty_cells.append((i, j))
                    continue
                    
                if not val.isdigit():
                    continue
                    
                num = int(val)
                
                validation_board[i][j] = 0
                if not SmartSudokuSolver.is_valid_move(validation_board, i, j, num):
                    conflicts.append((i, j))
                    self.cells[i][j].config(bg=COLORS['error_light'], fg=COLORS['error'])
                elif num != self.solution[i][j]:
                    incorrect.append((i, j))
                    self.cells[i][j].config(bg=COLORS['warning_light'], fg=COLORS['gray_800'])
                else:
                    self.cells[i][j].config(bg=COLORS['correct'], fg=COLORS['gray_900'])
                
                validation_board[i][j] = num
        
        if conflicts:
            messagebox.showerror(
                "❌ Rule Violations Found", 
                f"Found {len(conflicts)} cells that violate Sudoku rules (shown in red).\n"
                f"These cells have duplicate numbers in their row, column, or 3×3 box."
            )
        elif empty_cells:
            messagebox.showinfo(
                "📝 Puzzle Incomplete", 
                f"Great progress! You have {len(empty_cells)} empty cells remaining.\n"
                f"No rule violations found in your current entries."
            )
        elif incorrect:
            messagebox.showinfo(
                "🔍 Close, but not quite!", 
                f"No rule violations, but {len(incorrect)} cells don't match the solution (shown in yellow).\n"
                f"All your entries follow Sudoku rules correctly!"
            )
        else:
            self.on_puzzle_complete()

    def show_solution(self):
        """Display the complete solution"""
        if self.game_completed:
            messagebox.showinfo("Already Complete", "This puzzle is already solved!")
            return
            
        if messagebox.askyesno(
            "🔍 Show Complete Solution", 
            "This will reveal the entire solution and end the current game.\n\n"
            "Are you sure you want to continue?"
        ):
            self.timer_running = False
            
            for i in range(9):
                for j in range(9):
                    if self.cells[i][j]['state'] != 'readonly':
                        self.cells[i][j].delete(0, tk.END)
                        self.cells[i][j].insert(0, str(self.solution[i][j]))
                        self.cells[i][j].config(bg=COLORS['cyan_light'], fg=COLORS['gray_900'])
                        self.user_puzzle[i][j] = self.solution[i][j]
            
            messagebox.showinfo(
                "✅ Solution Revealed", 
                "The complete solution has been displayed.\n"
                "Start a new game to continue playing!"
            )

    def give_hint(self):
        """Provide an intelligent hint"""
        empty_cells = [(i, j) for i in range(9) for j in range(9) 
                      if self.user_puzzle[i][j] == 0]
        
        if not empty_cells:
            messagebox.showinfo("💡 No Hints Needed", "All cells are filled! Check your solution.")
            return
        
        best_cell = None
        min_possibilities = 10
        
        for i, j in empty_cells:
            possibilities = 0
            for num in range(1, 10):
                if SmartSudokuSolver.is_valid_move(self.user_puzzle, i, j, num):
                    possibilities += 1
            
            if 0 < possibilities < min_possibilities:
                min_possibilities = possibilities
                best_cell = (i, j)
        
        if best_cell:
            i, j = best_cell
            correct_value = self.solution[i][j]
            
            self.cells[i][j].delete(0, tk.END)
            self.cells[i][j].insert(0, str(correct_value))
            self.cells[i][j].config(bg=COLORS['hint_bg'], fg=COLORS['gray_900'])
            self.user_puzzle[i][j] = correct_value
            
            self.hints_used += 1
            self.hints_label.config(text=f"💡 Hints: {self.hints_used}")
            
            self.master.after(100, lambda: self.cells[i][j].config(bg=COLORS['warning_light']))
            self.master.after(500, lambda: self.cells[i][j].config(bg=COLORS['hint_bg']))
            
            messagebox.showinfo(
                "💡 Hint Provided!", 
                f"Added {correct_value} to row {i+1}, column {j+1}.\n"
                f"This cell had {min_possibilities} possible value(s)."
            )

    def clear_board(self):
        """Clear all user entries"""
        if messagebox.askyesno(
            "🗑 Clear All Entries", 
            "This will remove all your entries but keep the original puzzle clues.\n\n"
            "Are you sure you want to continue?"
        ):
            for i in range(9):
                for j in range(9):
                    if self.cells[i][j]['state'] != 'readonly':
                        self.cells[i][j].delete(0, tk.END)
                        self.cells[i][j].config(bg=COLORS['white'])
                        self.user_puzzle[i][j] = 0
            
            self.game_completed = False

    def load_from_file(self):
        """Load puzzle from file"""
        file_path = filedialog.askopenfilename(
            title="📁 Select Sudoku Puzzle File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()
            
            digits = ''.join(c for c in content if c.isdigit())
            
            if len(digits) != 81:
                messagebox.showerror(
                    "❌ Invalid File Format", 
                    f"File must contain exactly 81 digits.\n"
                    f"Found: {len(digits)} digits"
                )
                return
            
            preview_puzzle = []
            for i in range(9):
                row = []
                for j in range(9):
                    digit = int(digits[i * 9 + j])
                    if digit < 0 or digit > 9:
                        messagebox.showerror("❌ Invalid Digit", f"Found invalid digit: {digit}")
                        return
                    row.append(digit)
                preview_puzzle.append(row)
            
            self.show_puzzle_preview(preview_puzzle, file_path)
            
        except FileNotFoundError:
            messagebox.showerror("❌ File Error", "Could not find the selected file.")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to load file:\n{str(e)}")

    def show_puzzle_preview(self, preview_puzzle, file_path):
        """Show puzzle preview"""
        preview_window = tk.Toplevel(self.master)
        preview_window.title("📋 Puzzle Preview & Validation")
        preview_window.geometry("700x800")
        preview_window.configure(bg=COLORS['white'])
        preview_window.resizable(False, False)
        preview_window.transient(self.master)
        preview_window.grab_set()
        
        preview_window.update_idletasks()
        x = (preview_window.winfo_screenwidth() // 2) - 350
        y = (preview_window.winfo_screenheight() // 2) - 400
        preview_window.geometry(f"700x800+{x}+{y}")
        
        header_frame = tk.Frame(preview_window, bg=COLORS['primary'])
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text="📋 PUZZLE PREVIEW",
            font=('Segoe UI', 18, 'bold'),
            fg=COLORS['white'],
            bg=COLORS['primary'],
            pady=15
        ).pack()
        
        board_frame = tk.Frame(preview_window, bg=COLORS['gray_800'], relief='raised', bd=2)
        board_frame.pack(pady=20)
        
        preview_cells = [[None for _ in range(9)] for _ in range(9)]
        
        inner_board = tk.Frame(board_frame, bg=COLORS['gray_800'], padx=4, pady=4)
        inner_board.pack()
        
        for i in range(9):
            for j in range(9):
                padx = (2, 2)
                pady = (2, 2)
                
                if j % 3 == 2 and j != 8:
                    padx = (2, 6)
                if i % 3 == 2 and i != 8:
                    pady = (2, 6)
                
                cell = tk.Label(
                    inner_board,
                    text=str(preview_puzzle[i][j]) if preview_puzzle[i][j] != 0 else "",
                    width=3,
                    font=('Segoe UI', 14, 'bold'),
                    bg=COLORS['gray_100'] if preview_puzzle[i][j] != 0 else COLORS['white'],
                    fg=COLORS['gray_900'] if preview_puzzle[i][j] != 0 else COLORS['gray_400'],
                    relief='solid',
                    bd=1
                )
                cell.grid(row=i, column=j, padx=padx, pady=pady, ipady=4)
                preview_cells[i][j] = cell
        
        validation_frame = tk.Frame(preview_window, bg=COLORS['white'])
        validation_frame.pack(pady=20, fill="x", padx=20)
        
        self.validation_button = ModernButton(
            validation_frame,
            text="🔍 VALIDATE PUZZLE",
            command=lambda: self.validate_preview_puzzle(preview_puzzle, preview_cells, validation_frame, preview_window, file_path),
            bg_color=COLORS['warning'],
            font=('Segoe UI', 14, 'bold'),
            pady=12,
            padx=30
        )
        self.validation_button.pack(pady=10)
        
        self.blink_validation_button()
        
        info_text = tk.Label(
            validation_frame,
            text="⚠️ Please validate the puzzle before loading!\n"
                 "This will check for rule violations and solvability.",
            font=('Segoe UI', 12),
            fg=COLORS['gray_700'],
            bg=COLORS['white'],
            justify='center'
        )
        info_text.pack(pady=10)
        
        file_info = tk.Label(
            validation_frame,
            text=f"📁 File: {file_path}",
            font=('Segoe UI', 10),
            fg=COLORS['gray_600'],
            bg=COLORS['white']
        )
        file_info.pack(pady=5)

    def blink_validation_button(self):
        """Blink validation button"""
        if hasattr(self, 'validation_button') and self.validation_button.winfo_exists():
            current_color = self.validation_button['bg']
            new_color = COLORS['error'] if current_color == COLORS['warning'] else COLORS['warning']
            self.validation_button.config(bg=new_color)
            self.master.after(500, self.blink_validation_button)

    def validate_preview_puzzle(self, preview_puzzle, preview_cells, validation_frame, preview_window, file_path):
        """Validate the preview puzzle"""
        if hasattr(self, 'validation_button'):
            self.validation_button.config(bg=COLORS['primary'], text="🔄 VALIDATING...")
            self.validation_button.config(state='disabled')
        
        for widget in validation_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != validation_frame.winfo_children()[0]:
                widget.destroy()
        
        validation_errors = []
        conflict_cells = []
        
        for i in range(9):
            for j in range(9):
                if preview_puzzle[i][j] != 0:
                    num = preview_puzzle[i][j]
                    
                    for col in range(9):
                        if col != j and preview_puzzle[i][col] == num:
                            error_msg = f"Row {i+1}: Number {num} appears in columns {j+1} and {col+1}"
                            if error_msg not in validation_errors:
                                validation_errors.append(error_msg)
                            conflict_cells.extend([(i, j), (i, col)])
                    
                    for row in range(9):
                        if row != i and preview_puzzle[row][j] == num:
                            error_msg = f"Column {j+1}: Number {num} appears in rows {i+1} and {row+1}"
                            if error_msg not in validation_errors:
                                validation_errors.append(error_msg)
                            conflict_cells.extend([(i, j), (row, j)])
                    
                    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
                    for r in range(start_row, start_row + 3):
                        for c in range(start_col, start_col + 3):
                            if (r != i or c != j) and preview_puzzle[r][c] == num:
                                box_num = (i // 3) * 3 + (j // 3) + 1
                                error_msg = f"Box {box_num}: Number {num} appears at ({i+1},{j+1}) and ({r+1},{c+1})"
                                if error_msg not in validation_errors:
                                    validation_errors.append(error_msg)
                                conflict_cells.extend([(i, j), (r, c)])
        
        conflict_cells = list(set(conflict_cells))
        for i, j in conflict_cells:
            preview_cells[i][j].config(bg=COLORS['error_light'], fg=COLORS['error'])
        
        results_frame = tk.Frame(validation_frame, bg=COLORS['white'])
        results_frame.pack(pady=20, fill="x")
        
        if validation_errors:
            tk.Label(
                results_frame,
                text="❌ VALIDATION FAILED",
                font=('Segoe UI', 14, 'bold'),
                fg=COLORS['error'],
                bg=COLORS['white']
            ).pack()
            
            tk.Label(
                results_frame,
                text=f"Found {len(validation_errors)} rule violation(s):",
                font=('Segoe UI', 12),
                fg=COLORS['error'],
                bg=COLORS['white']
            ).pack(pady=5)
            
            error_frame = tk.Frame(results_frame, bg=COLORS['error_light'], relief='solid', bd=1)
            error_frame.pack(pady=10, padx=20, fill="x")
            
            for i, error in enumerate(validation_errors[:5]):
                tk.Label(
                    error_frame,
                    text=f"• {error}",
                    font=('Segoe UI', 10),
                    fg=COLORS['error'],
                    bg=COLORS['error_light'],
                    anchor='w'
                ).pack(fill="x", padx=10, pady=2)
            
            if len(validation_errors) > 5:
                tk.Label(
                    error_frame,
                    text=f"... and {len(validation_errors) - 5} more errors",
                    font=('Segoe UI', 10, 'italic'),
                    fg=COLORS['error'],
                    bg=COLORS['error_light']
                ).pack(pady=5)
            
            ModernButton(
                results_frame,
                text="📝 Fix Errors in File",
                command=preview_window.destroy,
                bg_color=COLORS['error'],
                font=('Segoe UI', 12, 'bold')
            ).pack(pady=10)
            
        else:
            test_board = copy.deepcopy(preview_puzzle)
            is_solvable = SmartSudokuSolver.solve(test_board)
            
            if is_solvable:
                solution_count = SmartSudokuSolver.count_solutions(preview_puzzle, 2)
                
                tk.Label(
                    results_frame,
                    text="✅ VALIDATION PASSED",
                    font=('Segoe UI', 14, 'bold'),
                    fg=COLORS['success'],
                    bg=COLORS['white']
                ).pack()
                
                clue_count = sum(1 for i in range(9) for j in range(9) if preview_puzzle[i][j] != 0)
                auto_difficulty = "expert" if clue_count < 25 else "hard" if clue_count < 30 else "medium" if clue_count < 35 else "easy"
                
                info_text = f"✓ No rule violations found\n✓ Puzzle is solvable\n"
                info_text += f"📊 Clues: {clue_count}/81\n📈 Difficulty: {auto_difficulty.title()}\n"
                info_text += f"🎯 Solutions: {solution_count} ({'Unique' if solution_count == 1 else 'Multiple'})"
                
                tk.Label(
                    results_frame,
                    text=info_text,
                    font=('Segoe UI', 11),
                    fg=COLORS['success'],
                    bg=COLORS['white'],
                    justify='center'
                ).pack(pady=10)
                
                ModernButton(
                    results_frame,
                    text="🚀 LOAD PUZZLE",
                    command=lambda: self.confirm_load_puzzle(preview_puzzle, test_board, preview_window),
                    bg_color=COLORS['success'],
                    font=('Segoe UI', 14, 'bold'),
                    pady=12,
                    padx=30
                ).pack(pady=15)
                
            else:
                tk.Label(
                    results_frame,
                    text="❌ PUZZLE UNSOLVABLE",
                    font=('Segoe UI', 14, 'bold'),
                    fg=COLORS['error'],
                    bg=COLORS['white']
                ).pack()
                
                tk.Label(
                    results_frame,
                    text="This puzzle has no valid solution.\nPlease check the input file.",
                    font=('Segoe UI', 12),
                    fg=COLORS['error'],
                    bg=COLORS['white'],
                    justify='center'
                ).pack(pady=10)
        
        if hasattr(self, 'validation_button'):
            self.validation_button.config(
                bg=COLORS['gray_500'], 
                text="✅ VALIDATED",
                state='disabled'
            )

    def confirm_load_puzzle(self, preview_puzzle, solution, preview_window):
        """Load the validated puzzle"""
        self.puzzle = preview_puzzle
        self.original_puzzle = copy.deepcopy(preview_puzzle)
        self.user_puzzle = copy.deepcopy(preview_puzzle)
        self.solution = solution
        
        self.update_board_display()
        
        self.hints_used = 0
        self.hints_label.config(text=f"💡 Hints: {self.hints_used}")
        self.game_completed = False
        self.reset_timer()
        
        preview_window.destroy()
        
        clue_count = sum(1 for i in range(9) for j in range(9) if preview_puzzle[i][j] != 0)
        messagebox.showinfo(
            "✅ Puzzle Loaded Successfully!", 
            f"🎯 Puzzle loaded and ready to solve!\n\n"
            f"📊 Clues provided: {clue_count}/81\n"
            f"🎮 Good luck solving it!"
        )

    def save_to_file(self):
        """Save current puzzle state"""
        file_path = filedialog.asksaveasfilename(
            title="💾 Save Sudoku Puzzle",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w') as file:
                puzzle_string = ""
                for i in range(9):
                    for j in range(9):
                        puzzle_string += str(self.user_puzzle[i][j])
                
                file.write(puzzle_string)
                
                file.write("\n\n# Formatted view:\n")
                for i in range(9):
                    row = ""
                    for j in range(9):
                        row += str(self.user_puzzle[i][j])
                        if j % 3 == 2 and j != 8:
                            row += " | "
                        elif j != 8:
                            row += " "
                    file.write(f"# {row}\n")
                    if i % 3 == 2 and i != 8:
                        file.write("# ------+-------+------\n")
            
            messagebox.showinfo(
                "💾 Save Successful", 
                f"Puzzle saved successfully!\n\n"
                f"📁 File: {file_path}"
            )
            
        except Exception as e:
            messagebox.showerror("❌ Save Error", f"Failed to save puzzle:\n{str(e)}")

    def update_board_display(self):
        """Update the visual display of the board"""
        for i in range(9):
            for j in range(9):
                entry = self.cells[i][j]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                
                if self.puzzle[i][j] != 0:
                    entry.insert(0, str(self.puzzle[i][j]))
                    entry.config(
                        state="readonly",
                        readonlybackground=COLORS['gray_200'],
                        fg=COLORS['gray_900'],
                        font=('Segoe UI', 24, 'bold')
                    )
                else:
                    entry.config(
                        bg=COLORS['white'], 
                        fg=self.button_color,
                        insertbackground=self.button_color
                    )
                    entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.on_cell_change(r, c))
                    entry.bind('<FocusIn>', lambda e, r=i, c=j: self.on_focus_in(r, c))
                    entry.bind('<FocusOut>', lambda e, r=i, c=j: self.on_focus_out(r, c))

    def new_game(self):
        """Start a new game"""
        if messagebox.askyesno(
            "🆕 New Game", 
            "Start a new game? Your current progress will be lost."
        ):
            self.puzzle, self.solution = generate_puzzle(self.difficulty)
            self.original_puzzle = copy.deepcopy(self.puzzle)
            self.user_puzzle = copy.deepcopy(self.puzzle)
            
            self.game_completed = False
            self.hints_used = 0
            self.hints_label.config(text=f"💡 Hints: {self.hints_used}")
            self.reset_timer()
            
            self.update_board_display()
            
            messagebox.showinfo(
                "🆕 New Game Started", 
                f"Fresh {self.difficulty} puzzle generated!\n"
                f"Good luck solving it!"
            )

    def change_difficulty(self, difficulty):
        """Change difficulty level"""
        self.difficulty = difficulty
        self.difficulty_label.config(text=f"📊 Level: {difficulty.title()}")
        
        # Update difficulty button colors
        difficulty_info = {
            "easy": COLORS['success'],
            "medium": COLORS['warning'],
            "hard": COLORS['error'],
            "expert": COLORS['gray_800']
        }
        
        for diff, (btn, orig_color) in self.diff_buttons_refs.items():
            if diff == difficulty:
                btn.config(bg=orig_color)
                btn.bg_color = orig_color
            else:
                btn.config(bg=COLORS['gray_400'])
                btn.bg_color = COLORS['gray_400']
        
        self.new_game()

    def reset_timer(self):
        """Reset timer based on mode"""
        if self.timer_mode.get() == "count_up":
            self.timer_seconds = 0
            self.timer_running = True
        elif self.timer_mode.get() == "count_down":
            self.timer_seconds = self.countdown_minutes.get() * 60
            self.timer_running = True
        else:
            self.timer_running = False
            self.timer_label.config(text="⏱ Free Play ∞")

    def start_timer(self):
        """Start the timer"""
        self.reset_timer()
        self.update_timer()

    def update_timer(self):
        """Update timer display"""
        if not self.game_completed:
            if self.timer_mode.get() == "count_up" and self.timer_running:
                minutes = self.timer_seconds // 60
                seconds = self.timer_seconds % 60
                self.timer_label.config(
                    text=f"⏱ {minutes:02d}:{seconds:02d}",
                    fg=self.button_color
                )
                self.timer_seconds += 1
                
            elif self.timer_mode.get() == "count_down" and self.timer_running:
                if self.timer_seconds > 0:
                    minutes = self.timer_seconds // 60
                    seconds = self.timer_seconds % 60
                    
                    if self.timer_seconds <= 60:
                        color = COLORS['error']
                    elif self.timer_seconds <= 300:
                        color = COLORS['warning']
                    else:
                        color = self.button_color
                    
                    self.timer_label.config(
                        text=f"⏱ {minutes:02d}:{seconds:02d}",
                        fg=color
                    )
                    self.timer_seconds -= 1
                else:
                    self.timer_running = False
                    self.timer_label.config(
                        text="⏱ Time's Up! ⏰",
                        fg=COLORS['error']
                    )
                    messagebox.showwarning(
                        "⏰ Time's Up!", 
                        "Your time has expired!\n\n"
                        "You can continue playing without time pressure,\n"
                        "or start a new game."
                    )
            elif self.timer_mode.get() == "free":
                self.timer_label.config(
                    text="⏱ Free Play ∞",
                    fg=COLORS['gray_600']
                )
        
        self.master.after(1000, self.update_timer)

    def show_help(self):
        """Display help dialog"""
        help_window = tk.Toplevel(self.master)
        help_window.title("❓ Sudoku Master - Help")
        help_window.geometry("600x700")
        help_window.configure(bg=COLORS['white'])
        help_window.resizable(False, False)
        help_window.transient(self.master)
        help_window.grab_set()
        
        header_frame = tk.Frame(help_window, bg=COLORS['primary'])
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text="🎯 SUDOKU MASTER - HELP",
            font=('Segoe UI', 20, 'bold'),
            fg=COLORS['white'],
            bg=COLORS['primary'],
            pady=15
        ).pack()
        
        content_frame = tk.Frame(help_window, bg=COLORS['white'])
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_area = tk.Text(
            content_frame,
            wrap="word",
            font=('Segoe UI', 11),
            bg=COLORS['gray_50'],
            fg=COLORS['gray_800'],
            padx=15,
            pady=15,
            relief="solid",
            bd=1
        )
        text_area.pack(fill="both", expand=True)
        
        help_content = """🎯 HOW TO PLAY SUDOKU

📋 BASIC RULES:
• Fill each row with numbers 1-9 (no duplicates)
• Fill each column with numbers 1-9 (no duplicates)
• Fill each 3×3 box with numbers 1-9 (no duplicates)

🎮 NEW FEATURES:

🎨 THEME CUSTOMIZATION:
• Change background color independently
• Change button colors separately
• Personalize your gaming experience

📥 DOWNLOAD SOLUTION:
• Save completed puzzles as .txt files
• Download full solution even if not complete
• Includes formatted view and statistics

🔍 AUTO-CHECK TOGGLE:
• Turn ON: See colors (green=correct, yellow=valid, red=wrong)
• Turn OFF: Play without hints, check at the end
• Toggle anytime during gameplay

⏰ CUSTOM COUNTDOWN:
• Set your own countdown timer (1-60 minutes)
• Choose Count Up, Count Down, or Free Play mode
• Timer changes color as time runs out

💡 SMART HINTS:
• Hints target cells with fewest possibilities
• Track hints used for scoring
• Yellow highlight for hint cells

🏆 DIFFICULTY LEVELS:
• Easy: 40+ clues
• Medium: 32+ clues
• Hard: 26+ clues
• Expert: 22+ clues

📁 FILE FORMAT (.txt):
• Exactly 81 digits in sequence
• 0 = empty, 1-9 = filled
• Example: 530070000600195000...

⌨️ CONTROLS:
• 1-9: Enter numbers
• Backspace/Delete: Clear cell
• Tab: Next cell

🎓 CREATED BY:
Mutaib • Andrie • Fawad
Universitas Syiah Kuala © 2025"""

        text_area.insert("1.0", help_content)
        text_area.config(state="disabled")
        
        ModernButton(
            help_window,
            text="✅ Got It!",
            command=help_window.destroy,
            bg_color=COLORS['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=15)

# ------------------- Main Application -------------------

def main():
    """Main application entry point"""
    root = tk.Tk()
    
    try:
        pass
    except:
        pass
    
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="📁 File", menu=file_menu)
    
    game_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="🎮 Game", menu=game_menu)
    
    settings_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="⚙️ Settings", menu=settings_menu)
    
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="❓ Help", menu=help_menu)
    
    game = SudokuGame(root)
    
    file_menu.add_command(label="🆕 New Game", command=lambda: game.new_game())
    file_menu.add_separator()
    file_menu.add_command(label="📁 Upload Puzzle", command=lambda: game.load_from_file())
    file_menu.add_command(label="💾 Save Puzzle", command=lambda: game.save_to_file())
    file_menu.add_command(label="📥 Download Solution", command=lambda: game.download_solution())
    file_menu.add_separator()
    file_menu.add_command(label="❌ Exit", command=root.quit)
    
    game_menu.add_command(label="✅ Check Solution", command=lambda: game.check_solution())
    game_menu.add_command(label="🔍 Show Solution", command=lambda: game.show_solution())
    game_menu.add_command(label="💡 Get Hint", command=lambda: game.give_hint())
    game_menu.add_separator()
    game_menu.add_command(label="🗑 Clear Board", command=lambda: game.clear_board())
    
    difficulty_menu = tk.Menu(settings_menu, tearoff=0)
    settings_menu.add_cascade(label="📊 Difficulty", menu=difficulty_menu)
    difficulty_menu.add_command(label="😊 Easy", command=lambda: game.change_difficulty("easy"))
    difficulty_menu.add_command(label="🙂 Medium", command=lambda: game.change_difficulty("medium"))
    difficulty_menu.add_command(label="😤 Hard", command=lambda: game.change_difficulty("hard"))
    difficulty_menu.add_command(label="🤯 Expert", command=lambda: game.change_difficulty("expert"))
    
    settings_menu.add_separator()
    settings_menu.add_command(label="🎨 Change Background", command=lambda: game.change_bg_color())
    settings_menu.add_command(label="🖌 Change Buttons", command=lambda: game.change_button_color())
    
    help_menu.add_command(label="📖 How to Play", command=lambda: game.show_help())
    help_menu.add_separator()
    help_menu.add_command(label="ℹ️ About", command=lambda: messagebox.showinfo(
        "About Sudoku Master",
        "🎯 Sudoku Master - Enhanced Edition\n\n"
        "Features:\n"
        "• Theme customization\n"
        "• Download solutions\n"
        "• Custom countdown timer\n"
        "• Auto-check toggle\n"
        "• Smart hints\n\n"
        "👨‍💻 Created by:\n"
        "MUTAIB • ANDRIE • FAWAD\n\n"
        "🏛 Universitas Syiah Kuala\n"
        "© 2025"
    ))
    
    root.update_idletasks()
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit Sudoku Master?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()