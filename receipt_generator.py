from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, Optional

class ReceiptGenerator:
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.black
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.black,
            backColor=colors.lightgrey
        ))
        

        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=20,
            # Adicione a linha abaixo
            leading=24, 
            spaceAfter=5,
            alignment=TA_LEFT
        ))
        

        self.styles.add(ParagraphStyle(
            name='Signature',
            parent=self.styles['Normal'],
            fontSize=20,
            alignment=TA_CENTER,
            spaceBefore=20
        ))
    
    def generate_receipt(self, data: Dict[str, Any]) -> Optional[BytesIO]:
        try:
            buffer = BytesIO()
            
            doc = SimpleDocTemplate(
                buffer,
                pagesize=(A4[1], A4[0]),  # Landscape orientation
                rightMargin=1.5*cm,
                leftMargin=1.5*cm,
                topMargin=1.5*cm,
                bottomMargin=1.5*cm
            )
            
            
            story = []
            
            
            story.extend(self._create_store_header(data))
            
            
            story.extend(self._create_main_info_section(data))
            
            
            story.extend(self._create_bottom_section(data))
            
            
            doc.build(story)
            
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            print(f"Erro ao gerar PDF: {str(e)}")
            return None
    
    def _create_store_header(self, data: Dict[str, Any]) -> list:
    
        story = []
        
        
        loja = data.get('loja', 'N/A')
        
        
        store_paragraph = Paragraph(
            f'<font color="red" size="48"><b>LOJA {loja}</b></font>',
            self.styles['CustomTitle']
        )
        story.append(store_paragraph)
        story.append(Spacer(1, 1*cm))
        
        return story
    
    def _create_main_info_section(self, data: Dict[str, Any]) -> list:
        
        story = []
        
        
        main_data = []
        
        
        destinatario_content = []
        destinatario_content.append("DESTINATÁRIO:")
        destinatario_content.append(data.get('destinatario_nome', 'N/A'))
        destinatario_content.append(f"{data.get('destinatario_endereco', 'N/A')} - {data.get('destinatario_bairro', 'N/A')}")
        destinatario_content.append(f"{data.get('destinatario_municipio', 'N/A')} – {data.get('destinatario_uf', 'N/A')} – CEP.: {data.get('destinatario_cep', 'N/A')}")
        destinatario_content.append(f"CNPJ: {data.get('destinatario_cnpj', 'N/A')} – I.E: {data.get('destinatario_ie', 'N/A')}")
        
        destinatario_paragraph = Paragraph("<br/>".join(destinatario_content), self.styles['CustomNormal'])
        main_data.append([destinatario_paragraph])
        
        
        main_data.append([Paragraph("<hr/>", self.styles['CustomNormal'])])
        
        
        #main_data.append([Spacer(1, 0.3*cm)])
        
       
        remetente_content = []
        remetente_content.append('<font color="red"><b>SUPORTE TECNICO</b></font>')
        remetente_content.append('')
        remetente_content.append("REMETENTE:")
        remetente_content.append(data.get('remetente_nome', 'N/A'))
        remetente_content.append(f"{data.get('remetente_endereco', 'N/A')} - {data.get('remetente_bairro', 'N/A')} - {data.get('remetente_municipio', 'N/A')} – {data.get('remetente_uf', 'N/A')}")
        remetente_content.append(f"CEP: {data.get('remetente_cep', 'N/A')} CNPJ: {data.get('remetente_cnpj', 'N/A')} – I.E.: {data.get('remetente_ie', 'N/A')}")
        
        remetente_paragraph = Paragraph("<br/>".join(remetente_content), self.styles['CustomNormal'])
        main_data.append([remetente_paragraph])
        
        
        table = Table(main_data, colWidths=[25*cm])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 1*cm))
        
        return story
    
    def _create_bottom_section(self, data: Dict[str, Any]) -> list:
        
        story = []
        
        
        nf_number = data.get('numero_nfe', 'N/A')
        volume_number = data.get('volume_number', '1/1') 
        
        
        nf_content = []
        nf_content.append(Paragraph("SOB NOTA FISCAL", self.styles['CustomNormal']))
        nf_content.append(Paragraph(f'Nº <font size="24" color="blue"><b>{nf_number}</b></font>', self.styles['CustomNormal']))
        
         
        fragil_content = []
        fragil_content.append(Paragraph('<font size="36" color="red"><b>FRÁGIL</b></font>', self.styles['CustomTitle']))
        
        
        volume_content = []
        volume_content.append(Paragraph("Nº DE VOLUME", self.styles['CustomNormal']))
        volume_content.append(Paragraph(f'<font color="red">«Nº» <font size="24"><b>{volume_number}</b></font></font>', self.styles['CustomNormal']))
        
        
        bottom_data = [
            [
                Table([[paragraph] for paragraph in nf_content], colWidths=[8*cm]),
                Table([[paragraph] for paragraph in fragil_content], colWidths=[6*cm]),
                Table([[paragraph] for paragraph in volume_content], colWidths=[8*cm])
            ]
        ]
        
        
        bottom_table = Table(bottom_data, colWidths=[8*cm, 6*cm, 8*cm])
        bottom_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),   
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),     
            ('ALIGN', (2, 0), (2, 0), 'CENTER'),   
            ('GRID', (0, 0), (0, 0), 1, colors.black),  
            ('GRID', (2, 0), (2, 0), 1, colors.black),  
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(bottom_table)
        
        return story
    

