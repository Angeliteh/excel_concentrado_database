"""
🔍 VENTANA DE DETALLES DE VALIDACIÓN
===================================

Ventana dedicada para mostrar los resultados de validación de forma organizada,
responsive y fácil de navegar con múltiples columnas y scroll.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QScrollArea, 
                             QWidget, QLabel, QFrame, QGridLayout, QPushButton,
                             QTabWidget, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ValidationDetailsWindow(QDialog):
    """
    Ventana dedicada para mostrar detalles de validación de forma organizada.
    
    Características:
    - Layout responsive con múltiples columnas
    - Scroll para contenido largo
    - Organización por pestañas/secciones
    - Aprovecha mejor el espacio horizontal
    """
    
    def __init__(self, reporte, nombre_archivo, parent=None):
        super().__init__(parent)
        self.reporte = reporte
        self.nombre_archivo = nombre_archivo
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializar interfaz de la ventana."""
        self.setWindowTitle(f"🔍 Detalles de Validación - {self.nombre_archivo}")
        self.resize(1000, 700)  # Ventana más grande
        self.setModal(True)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header con resumen
        self.crear_header(layout)
        
        # Tabs para organizar contenido
        self.crear_tabs(layout)
        
        # Botones de acción
        self.crear_botones(layout)
        
        self.setLayout(layout)
    
    def crear_header(self, layout):
        """Crear header con información general."""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # Título
        titulo = QLabel(f"🔍 AUDITORÍA: {self.nombre_archivo}")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(titulo)
        
        header_layout.addStretch()
        
        # Estadísticas
        stats_layout = QVBoxLayout()
        
        exitosas_label = QLabel(f"✅ Exitosas: {self.reporte['total_validaciones_exitosas']}")
        exitosas_label.setFont(QFont("Arial", 11, QFont.Bold))
        exitosas_label.setStyleSheet("color: #27ae60;")
        stats_layout.addWidget(exitosas_label)
        
        discrepancias_label = QLabel(f"⚠️ Discrepancias: {self.reporte['total_discrepancias']}")
        discrepancias_label.setFont(QFont("Arial", 11, QFont.Bold))
        discrepancias_label.setStyleSheet("color: #e74c3c;")
        stats_layout.addWidget(discrepancias_label)
        
        header_layout.addLayout(stats_layout)
        
        layout.addWidget(header_frame)
    
    def crear_tabs(self, layout):
        """Crear pestañas para organizar el contenido."""
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 4px 4px 0 0;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
        """)
        
        # Tab 1: Subtotales
        self.crear_tab_subtotales()
        
        # Tab 2: Totales
        self.crear_tab_totales()
        
        # Tab 3: Coherencia
        self.crear_tab_coherencia()
        
        # Tab 4: Resumen completo (si se necesita)
        self.crear_tab_resumen()
        
        layout.addWidget(self.tabs)
    
    def crear_tab_subtotales(self):
        """Crear pestaña de subtotales con layout de columnas."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Título de sección
        titulo = QLabel("📊 SUBTOTALES (H = Hombres, M = Mujeres)")
        titulo.setFont(QFont("Arial", 12, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # Scroll area para contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget contenedor con grid layout
        contenido = QWidget()
        self.grid_subtotales = QGridLayout(contenido)
        self.grid_subtotales.setSpacing(15)
        
        scroll.setWidget(contenido)
        layout.addWidget(scroll)
        
        self.tabs.addTab(tab, "📊 Subtotales")
    
    def crear_tab_totales(self):
        """Crear pestaña de totales."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        titulo = QLabel("🧮 TOTALES (Subtotal H + Subtotal M)")
        titulo.setFont(QFont("Arial", 12, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        contenido = QWidget()
        self.grid_totales = QGridLayout(contenido)
        self.grid_totales.setSpacing(15)
        
        scroll.setWidget(contenido)
        layout.addWidget(scroll)
        
        self.tabs.addTab(tab, "🧮 Totales")
    
    def crear_tab_coherencia(self):
        """Crear pestaña de coherencia."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        titulo = QLabel("🔄 COHERENCIA (Existencia = Inscripción - Bajas)")
        titulo.setFont(QFont("Arial", 12, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        contenido = QWidget()
        self.grid_coherencia = QGridLayout(contenido)
        self.grid_coherencia.setSpacing(10)
        
        scroll.setWidget(contenido)
        layout.addWidget(scroll)
        
        self.tabs.addTab(tab, "🔄 Coherencia")
    
    def crear_tab_resumen(self):
        """Crear pestaña de resumen completo."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        titulo = QLabel("📋 RESUMEN COMPLETO")
        titulo.setFont(QFont("Arial", 12, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # Text area con scroll automático
        self.text_resumen = QTextEdit()
        self.text_resumen.setReadOnly(True)
        self.text_resumen.setFont(QFont("Consolas", 11))
        self.text_resumen.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        
        layout.addWidget(self.text_resumen)
        
        self.tabs.addTab(tab, "📋 Resumen")
    
    def crear_botones(self, layout):
        """Crear botones de acción."""
        botones_layout = QHBoxLayout()
        botones_layout.addStretch()
        
        # Botón cerrar
        btn_cerrar = QPushButton("✅ Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        btn_cerrar.clicked.connect(self.accept)
        botones_layout.addWidget(btn_cerrar)
        
        layout.addLayout(botones_layout)
    
    def cargar_datos(self):
        """Cargar datos en las pestañas."""
        # Organizar validaciones por tipo
        exitosas = self._organizar_por_tipo(self.reporte['validaciones_exitosas'])
        discrepancias = self._organizar_por_tipo(self.reporte['discrepancias'])
        
        # Cargar cada pestaña
        self.cargar_subtotales(exitosas, discrepancias)
        self.cargar_totales(exitosas, discrepancias)
        self.cargar_coherencia(exitosas, discrepancias)
        self.cargar_resumen()
    
    def _organizar_por_tipo(self, validaciones):
        """Organizar validaciones por tipo y concepto."""
        organizadas = {}
        for val in validaciones:
            tipo = val['tipo']
            concepto = val['concepto']
            
            if tipo not in organizadas:
                organizadas[tipo] = {}
            if concepto not in organizadas[tipo]:
                organizadas[tipo][concepto] = []
            
            organizadas[tipo][concepto].append(val)
        
        return organizadas
    
    def cargar_subtotales(self, exitosas, discrepancias):
        """Cargar datos de subtotales en grid de 3 columnas con orden específico."""
        # Orden específico requerido - MOSTRAR TODOS para consistencia
        orden_conceptos = [
            'INSCRIPCIÓN', 'BAJAS', 'EXISTENCIA', 'ALTAS',
            'APROBADOS', 'REPROBADOS', 'BECADOS MUNICIPIO',
            'BECADOS SEED', 'BIENESTAR', 'GRUPOS'
        ]

        row = 0
        col = 0
        max_cols = 3

        # Mostrar TODOS los conceptos excepto GRUPOS (que no tiene subtotales H/M)
        for concepto in orden_conceptos:
            if concepto != 'GRUPOS':  # Filtrar GRUPOS de subtotales
                frame = self.crear_frame_concepto(concepto, exitosas, discrepancias, ['SUBTOTAL_H', 'SUBTOTAL_M'])
                self.grid_subtotales.addWidget(frame, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def cargar_totales(self, exitosas, discrepancias):
        """Cargar datos de totales con orden específico."""
        # Orden específico requerido
        orden_conceptos = [
            'INSCRIPCIÓN', 'BAJAS', 'EXISTENCIA', 'ALTAS',
            'APROBADOS', 'REPROBADOS', 'BECADOS MUNICIPIO',
            'BECADOS SEED', 'BIENESTAR', 'GRUPOS'
        ]

        # Obtener conceptos disponibles
        conceptos_disponibles = set()
        for tipo in ['TOTAL', 'TOTAL_GRUPOS']:
            if tipo in exitosas:
                conceptos_disponibles.update(exitosas[tipo].keys())
            if tipo in discrepancias:
                conceptos_disponibles.update(discrepancias[tipo].keys())

        # Filtrar y ordenar según el orden específico
        conceptos_ordenados = [c for c in orden_conceptos if c in conceptos_disponibles]

        row = 0
        col = 0
        max_cols = 3

        for concepto in conceptos_ordenados:
            frame = self.crear_frame_concepto(concepto, exitosas, discrepancias, ['TOTAL', 'TOTAL_GRUPOS'])
            self.grid_totales.addWidget(frame, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def cargar_coherencia(self, exitosas, discrepancias):
        """Cargar datos de coherencia organizados por grados."""
        conceptos = set()
        if 'COHERENCIA_EXISTENCIA' in exitosas:
            conceptos.update(exitosas['COHERENCIA_EXISTENCIA'].keys())
        if 'COHERENCIA_EXISTENCIA' in discrepancias:
            conceptos.update(discrepancias['COHERENCIA_EXISTENCIA'].keys())

        # Organizar por grados
        grados_organizados = self._organizar_conceptos_por_grados(conceptos)

        row = 0

        # Crear frames por grado
        for grado, conceptos_grado in grados_organizados.items():
            if conceptos_grado:  # Solo si hay conceptos para este grado
                frame_grado = self.crear_frame_grado_coherencia(grado, conceptos_grado, exitosas, discrepancias)
                self.grid_coherencia.addWidget(frame_grado, row, 0, 1, 3)  # Span 3 columnas
                row += 1

    def _organizar_conceptos_por_grados(self, conceptos):
        """Organizar conceptos de coherencia por grados."""
        grados = {
            '1er Grado': [],
            '2do Grado': [],
            '3er Grado': [],
            '4to Grado': [],
            '5to Grado': [],
            '6to Grado': []
        }

        for concepto in conceptos:
            if '1O.' in concepto or '1ER' in concepto:
                grados['1er Grado'].append(concepto)
            elif '2O.' in concepto or '2DO' in concepto:
                grados['2do Grado'].append(concepto)
            elif '3O.' in concepto or '3ER' in concepto:
                grados['3er Grado'].append(concepto)
            elif '4O.' in concepto or '4TO' in concepto:
                grados['4to Grado'].append(concepto)
            elif '5O.' in concepto or '5TO' in concepto:
                grados['5to Grado'].append(concepto)
            elif '6O.' in concepto or '6TO' in concepto:
                grados['6to Grado'].append(concepto)

        return grados
    
    def crear_frame_concepto(self, concepto, exitosas, discrepancias, tipos):
        """Crear frame para un concepto específico."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(4)
        
        # Título del concepto
        titulo = QLabel(f"🎯 {concepto}")
        titulo.setFont(QFont("Arial", 12, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50;")
        layout.addWidget(titulo)
        
        # Datos por tipo - LÓGICA ESPECIAL PARA GRUPOS
        for tipo in tipos:
            tipo_label = tipo.replace('SUBTOTAL_', '').replace('TOTAL_', '').replace('TOTAL', 'Total')

            # 🎯 LÓGICA ESPECIAL: GRUPOS solo tiene TOTAL_GRUPOS, no TOTAL normal
            if concepto == 'GRUPOS' and tipo == 'TOTAL':
                continue  # Saltar TOTAL normal para GRUPOS
            elif concepto != 'GRUPOS' and tipo == 'TOTAL_GRUPOS':
                continue  # Saltar TOTAL_GRUPOS para conceptos normales

            if tipo in exitosas and concepto in exitosas[tipo]:
                val = exitosas[tipo][concepto][0]

                # Etiqueta especial para GRUPOS
                if concepto == 'GRUPOS' and tipo == 'TOTAL_GRUPOS':
                    tipo_label = 'Total (suma directa)'

                # Mostrar valor y descripción si está disponible
                if 'descripcion' in val and '=' in val['descripcion']:
                    # Extraer la parte del cálculo
                    desc_parts = val['descripcion'].split('=')
                    if len(desc_parts) >= 2:
                        # Obtener la operación (antes del =)
                        operacion = desc_parts[0].split(':')[-1].strip()
                        # Obtener el resultado (después del =, antes de cualquier paréntesis)
                        resultado = desc_parts[1].split('(')[0].strip()

                        label = QLabel(f"✅ {tipo_label}: {val['valor']}")
                        label.setStyleSheet("color: #27ae60; font-size: 11px; font-weight: bold;")
                        layout.addWidget(label)

                        # Agregar línea con el cálculo completo
                        calc_label = QLabel(f"   {operacion} = {resultado}")
                        calc_label.setStyleSheet("color: #6c757d; font-size: 10px;")
                        layout.addWidget(calc_label)
                    else:
                        label = QLabel(f"✅ {tipo_label}: {val['valor']}")
                        label.setStyleSheet("color: #27ae60; font-size: 11px;")
                        layout.addWidget(label)
                else:
                    label = QLabel(f"✅ {tipo_label}: {val['valor']}")
                    label.setStyleSheet("color: #27ae60; font-size: 11px;")
                    layout.addWidget(label)

            elif tipo in discrepancias and concepto in discrepancias[tipo]:
                disc = discrepancias[tipo][concepto][0]

                # Etiqueta especial para GRUPOS
                if concepto == 'GRUPOS' and tipo == 'TOTAL_GRUPOS':
                    tipo_label = 'Total (suma directa)'

                label = QLabel(f"❌ {tipo_label}: {disc['valor_reportado']} ≠ {disc['valor_calculado']}")
                label.setStyleSheet("color: #e74c3c; font-size: 11px;")
                layout.addWidget(label)

                # Mostrar operación si está disponible en la descripción
                if 'descripcion' in disc and '=' in disc['descripcion']:
                    desc_parts = disc['descripcion'].split('=')
                    if len(desc_parts) >= 2:
                        operacion = desc_parts[0].split(':')[-1].strip()
                        resultado = desc_parts[1].strip()

                        calc_label = QLabel(f"   Calculado: {operacion} = {resultado}")
                        calc_label.setStyleSheet("color: #e74c3c; font-size: 10px;")
                        layout.addWidget(calc_label)

                # Mostrar diferencia
                if 'diferencia' in disc:
                    diff_label = QLabel(f"   Diferencia: {disc['diferencia']:.2f}")
                    diff_label.setStyleSheet("color: #e74c3c; font-size: 10px;")
                    layout.addWidget(diff_label)
            else:
                # Mensaje especial para GRUPOS en subtotales
                if concepto == 'GRUPOS' and tipo in ['SUBTOTAL_H', 'SUBTOTAL_M']:
                    label = QLabel(f"ℹ️ GRUPOS no tiene subtotales H/M")
                    label.setStyleSheet("color: #17a2b8; font-size: 11px; font-style: italic;")
                    layout.addWidget(label)

                    label2 = QLabel(f"   Se calcula como suma directa")
                    label2.setStyleSheet("color: #17a2b8; font-size: 10px; font-style: italic;")
                    layout.addWidget(label2)
                # Concepto sin datos - SOLO para conceptos normales, no GRUPOS
                elif not (concepto == 'GRUPOS' and tipo == 'TOTAL') and not (concepto != 'GRUPOS' and tipo == 'TOTAL_GRUPOS'):
                    label = QLabel(f"📊 {tipo_label}: 0.0")
                    label.setStyleSheet("color: #6c757d; font-size: 11px;")
                    layout.addWidget(label)
        
        return frame
    
    def crear_frame_coherencia(self, concepto, exitosas, discrepancias):
        """Crear frame para coherencia con altura automática."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
                margin: 2px;
                min-height: 70px;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setSpacing(4)

        # Título
        titulo = QLabel(concepto)
        titulo.setFont(QFont("Arial", 9, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50;")
        titulo.setWordWrap(True)
        layout.addWidget(titulo)

        # Estado con detalles
        if 'COHERENCIA_EXISTENCIA' in exitosas and concepto in exitosas['COHERENCIA_EXISTENCIA']:
            val = exitosas['COHERENCIA_EXISTENCIA'][concepto][0]
            estado = QLabel("✅ Correcto")
            estado.setStyleSheet("color: #27ae60; font-size: 9px; font-weight: bold;")
            layout.addWidget(estado)

            # Mostrar la fórmula si está disponible
            if 'descripcion' in val:
                desc = val['descripcion'].replace('✅ Coherencia ', '').replace(concepto + ': ', '')
                formula = QLabel(desc)
                formula.setStyleSheet("color: #6c757d; font-size: 8px;")
                formula.setWordWrap(True)
                layout.addWidget(formula)
        else:
            if 'COHERENCIA_EXISTENCIA' in discrepancias and concepto in discrepancias['COHERENCIA_EXISTENCIA']:
                disc = discrepancias['COHERENCIA_EXISTENCIA'][concepto][0]
                estado = QLabel("❌ Error")
                estado.setStyleSheet("color: #e74c3c; font-size: 9px; font-weight: bold;")
                layout.addWidget(estado)

                # Mostrar detalles del error
                if 'descripcion' in disc:
                    desc = disc['descripcion']
                    error_desc = QLabel(desc)
                    error_desc.setStyleSheet("color: #e74c3c; font-size: 8px;")
                    error_desc.setWordWrap(True)
                    layout.addWidget(error_desc)

        layout.addStretch()
        return frame

    def crear_frame_grado_coherencia(self, grado, conceptos_grado, exitosas, discrepancias):
        """Crear frame para un grado específico con sus H y M."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 12px;
                margin: 4px;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setSpacing(8)

        # Título del grado
        titulo_grado = QLabel(f"📚 {grado}")
        titulo_grado.setFont(QFont("Arial", 11, QFont.Bold))
        titulo_grado.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        layout.addWidget(titulo_grado)

        # Layout horizontal para H y M
        hm_layout = QHBoxLayout()
        hm_layout.setSpacing(15)

        # Separar H y M
        conceptos_h = [c for c in conceptos_grado if c.startswith('H-')]
        conceptos_m = [c for c in conceptos_grado if c.startswith('M-')]

        # Frame para Hombres
        if conceptos_h:
            frame_h = self.crear_frame_genero_coherencia('👨 Hombres', conceptos_h, exitosas, discrepancias)
            hm_layout.addWidget(frame_h)

        # Frame para Mujeres
        if conceptos_m:
            frame_m = self.crear_frame_genero_coherencia('👩 Mujeres', conceptos_m, exitosas, discrepancias)
            hm_layout.addWidget(frame_m)

        layout.addLayout(hm_layout)
        return frame

    def crear_frame_genero_coherencia(self, titulo_genero, conceptos, exitosas, discrepancias):
        """Crear frame para un género específico (H o M)."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 8px;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setSpacing(4)

        # Título del género
        titulo = QLabel(titulo_genero)
        titulo.setFont(QFont("Arial", 11, QFont.Bold))
        titulo.setStyleSheet("color: #495057;")
        layout.addWidget(titulo)

        # Procesar cada concepto
        for concepto in conceptos:
            if 'COHERENCIA_EXISTENCIA' in exitosas and concepto in exitosas['COHERENCIA_EXISTENCIA']:
                val = exitosas['COHERENCIA_EXISTENCIA'][concepto][0]

                # Estado
                estado = QLabel("✅ Coherente")
                estado.setStyleSheet("color: #27ae60; font-size: 11px; font-weight: bold;")
                layout.addWidget(estado)

                # Fórmula más legible
                if 'descripcion' in val:
                    desc = val['descripcion']
                    # Limpiar y hacer más legible
                    desc_limpia = desc.replace('✅ Coherencia ', '').replace(concepto + ': ', '')

                    # Hacer más legible la fórmula
                    if '=' in desc_limpia:
                        partes = desc_limpia.split('=')
                        if len(partes) >= 3:
                            existencia = partes[0].strip()
                            inscripcion = partes[1].strip()
                            bajas = partes[2].strip()

                            formula = QLabel(f"Existencia {existencia}")
                            formula.setStyleSheet("color: #2c3e50; font-size: 12px; font-weight: bold;")
                            layout.addWidget(formula)

                            calculo = QLabel(f"= Inscripción {inscripcion} - Bajas {bajas}")
                            calculo.setStyleSheet("color: #6c757d; font-size: 11px;")
                            layout.addWidget(calculo)
                        else:
                            formula = QLabel(desc_limpia)
                            formula.setStyleSheet("color: #6c757d; font-size: 11px;")
                            formula.setWordWrap(True)
                            layout.addWidget(formula)

            elif 'COHERENCIA_EXISTENCIA' in discrepancias and concepto in discrepancias['COHERENCIA_EXISTENCIA']:
                disc = discrepancias['COHERENCIA_EXISTENCIA'][concepto][0]

                estado = QLabel("❌ Error")
                estado.setStyleSheet("color: #e74c3c; font-size: 11px; font-weight: bold;")
                layout.addWidget(estado)

                # Mostrar detalles del error
                if 'descripcion' in disc:
                    desc = disc['descripcion']
                    error_desc = QLabel(desc)
                    error_desc.setStyleSheet("color: #e74c3c; font-size: 11px;")
                    error_desc.setWordWrap(True)
                    layout.addWidget(error_desc)

        return frame
    
    def cargar_resumen(self):
        """Cargar resumen completo en formato texto."""
        resumen = f"🔍 AUDITORÍA COMPLETA: {self.nombre_archivo}\n\n"
        resumen += f"✅ Validaciones exitosas: {self.reporte['total_validaciones_exitosas']}\n"
        resumen += f"⚠️ Discrepancias encontradas: {self.reporte['total_discrepancias']}\n\n"
        resumen += self.reporte['resumen']
        
        self.text_resumen.setPlainText(resumen)
