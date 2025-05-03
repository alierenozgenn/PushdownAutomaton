class PDA:
    def __init__(self):
        self.stack = []
        self.current_state = 'q0'
        self.state_history = []
        self.stack_history = []
        self.current_char = None
        self.save_state()
    
    def save_state(self):
        """Mevcut durumu ve stack'i kaydet"""
        self.state_history.append(self.current_state)
        self.stack_history.append(self.stack.copy())
    
    def transition(self, char):
        """Otomatın durumunu güncelleyen geçiş fonksiyonu"""
        self.current_char = char
        
        if self.current_state == 'q0':  # Başlangıç durumu
            if char == '(':
                self.stack.append(char)
                self.current_state = 'q1'
            elif char.isdigit():
                self.current_state = 'q2'
            else:
                self.current_state = 'rejected'
        
        elif self.current_state == 'q1':  # Parantez açıldıktan sonra
            if char == '(':
                self.stack.append(char)
            elif char.isdigit():
                self.current_state = 'q2'
            else:
                self.current_state = 'rejected'
        
        elif self.current_state == 'q2':  # Rakam gördükten sonra
            if char in '+-*/':
                self.current_state = 'q3'
            elif char == ')':
                if self.stack and self.stack[-1] == '(':
                    self.stack.pop()
                    self.current_state = 'q4'
                else:
                    self.current_state = 'rejected'
            elif char.isdigit():
                pass  # Aynı durumda kalır
            else:
                self.current_state = 'rejected'
        
        elif self.current_state == 'q3':  # Operatör gördükten sonra
            if char == '(':
                self.stack.append(char)
                self.current_state = 'q1'
            elif char.isdigit():
                self.current_state = 'q2'
            else:
                self.current_state = 'rejected'
        
        elif self.current_state == 'q4':  # Parantez kapandıktan sonra
            if char in '+-*/':
                self.current_state = 'q3'
            elif char == ')':
                if self.stack and self.stack[-1] == '(':
                    self.stack.pop()
                else:
                    self.current_state = 'rejected'
            else:
                self.current_state = 'rejected'
        
        self.save_state()
        return self.current_state, self.stack.copy()
    
    def is_accepted(self, expression):
        """İfadenin kabul edilip edilmediğini kontrol eder"""
        self.reset()
        
        for char in expression:
            self.transition(char)
            if self.current_state == 'rejected':
                return False
        
        return self.current_state in {'q2', 'q4'} and not self.stack
    
    def reset(self):
        """Otomatı başlangıç durumuna sıfırlar"""
        self.stack = []
        self.current_state = 'q0'
        self.state_history = []
        self.stack_history = []
        self.current_char = None
        self.save_state()
    
    def simulate_step_by_step(self, expression):
        """İfadeyi adım adım simüle eder ve her adımın sonuçlarını döndürür"""
        self.reset()
        results = []
        
        for i, char in enumerate(expression):
            state, stack = self.transition(char)
            results.append({
                'index': i,
                'char': char,
                'state': state,
                'stack': stack.copy(),
                'valid': state != 'rejected'
            })
            
            if state == 'rejected':
                break
                
        # Son durumun kabul edilebilir olup olmadığını kontrol et
        final_valid = self.current_state in {'q2', 'q4'} and not self.stack
        
        return results, final_valid
    
    def get_state_description(self, state):
        """Durum açıklamasını döndürür"""
        descriptions = {
            'q0': "Başlangıç durumu",
            'q1': "Parantez açıldıktan sonra",
            'q2': "Rakam görüldükten sonra",
            'q3': "Operatör görüldükten sonra",
            'q4': "Parantez kapandıktan sonra",
            'rejected': "Reddedildi"
        }
        return descriptions.get(state, "Bilinmeyen durum")
    
    def get_state_history(self):
        """Durum geçmişini döndürür"""
        return self.state_history
    
    def get_stack_history(self):
        """Stack geçmişini döndürür"""
        return self.stack_history