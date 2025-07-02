import streamlit as st
import tempfile
import os
from danfe_extractor import DANFEExtractor
from receipt_generator import ReceiptGenerator
from docx_generator import DOCXGenerator
import base64

def main():
    st.set_page_config(
        page_title="Gerador de Capa de Recebimento DANFE",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Gerador de Capa de Recebimento DANFE")
    st.markdown("---")
    

    st.header("🔄 Upload e Extração")
    
    uploaded_files = st.file_uploader(
        "Escolha os arquivos PDF das DANFEs",
        type=['pdf'],
        accept_multiple_files=True,
        help="Selecione um ou mais arquivos PDF contendo DANFEs"
    )
    
    if uploaded_files:
        if 'all_extracted_data' not in st.session_state:
            st.session_state.all_extracted_data = []
        
        if st.button("🔄 Processar Todos os PDFs", type="primary"):
            st.session_state.all_extracted_data = []
            extractor = DANFEExtractor()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                progress = (i + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"Processando {uploaded_file.name}...")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                try:
                    extracted_data = extractor.extract_from_pdf(tmp_file_path)
                    if extracted_data:
                        extracted_data['filename'] = uploaded_file.name
                        st.session_state.all_extracted_data.append(extracted_data)
                        st.success(f"✅ {uploaded_file.name} processado com sucesso!")
                    else:
                        st.error(f"❌ Erro ao processar {uploaded_file.name}")
                        
                except Exception as e:
                    st.error(f"❌ Erro em {uploaded_file.name}: {str(e)}")
                
                finally:
                    if os.path.exists(tmp_file_path):
                        os.unlink(tmp_file_path)
            
            progress_bar.empty()
            status_text.empty()
            st.session_state.files_processed = True
    
    if hasattr(st.session_state, 'all_extracted_data') and st.session_state.all_extracted_data:
        st.markdown("---")
        st.header("📊 Dados Extraídos e Edição")
        
        if len(st.session_state.all_extracted_data) > 1:
            selected_file = st.selectbox(
                "Selecione o arquivo para editar:",
                options=range(len(st.session_state.all_extracted_data)),
                format_func=lambda x: st.session_state.all_extracted_data[x]['filename']
            )
        else:
            selected_file = 0
        
        data = st.session_state.all_extracted_data[selected_file]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🏢 Informações do Destinatário")
            data['destinatario_nome'] = st.text_input("Nome/Razão Social", value=data.get('destinatario_nome', ''))
            data['destinatario_cnpj'] = st.text_input("CNPJ", value=data.get('destinatario_cnpj', ''))
            data['destinatario_endereco'] = st.text_input("Endereço", value=data.get('destinatario_endereco', ''))
            data['destinatario_bairro'] = st.text_input("Bairro", value=data.get('destinatario_bairro', ''))
            
            col1a, col1b = st.columns(2)
            with col1a:
                data['destinatario_municipio'] = st.text_input("Município", value=data.get('destinatario_municipio', ''))
                data['destinatario_cep'] = st.text_input("CEP", value=data.get('destinatario_cep', ''))
            with col1b:
                data['destinatario_uf'] = st.text_input("UF", value=data.get('destinatario_uf', ''))
                data['destinatario_ie'] = st.text_input("Inscrição Estadual", value=data.get('destinatario_ie', ''))
            
            data['loja'] = st.text_input("Loja", value=data.get('loja', ''))
        
        with col2:
            st.subheader("🏭 Informações do Remetente")
            data['remetente_nome'] = st.text_input("Nome Remetente", value=data.get('remetente_nome', ''))
            data['remetente_cnpj'] = st.text_input("CNPJ Remetente", value=data.get('remetente_cnpj', ''))
            data['remetente_endereco'] = st.text_input("Endereço Remetente", value=data.get('remetente_endereco', ''))
            
            col2a, col2b = st.columns(2)
            with col2a:
                data['remetente_municipio'] = st.text_input("Município Remetente", value=data.get('remetente_municipio', ''))
                data['remetente_cep'] = st.text_input("CEP Remetente", value=data.get('remetente_cep', ''))
            with col2b:
                data['remetente_uf'] = st.text_input("UF Remetente", value=data.get('remetente_uf', ''))
                data['remetente_ie'] = st.text_input("I.E. Remetente", value=data.get('remetente_ie', ''))
        
        st.subheader("📄 Informações da Nota Fiscal")
        col3a, col3b, col3c = st.columns(3)
        
        with col3a:
            data['numero_nfe'] = st.text_input("Número NF-e", value=data.get('numero_nfe', ''))
            data['serie'] = st.text_input("Série", value=data.get('serie', ''))
        
        with col3b:
            data['data_emissao'] = st.text_input("Data de Emissão", value=data.get('data_emissao', ''))
            data['valor_total'] = st.text_input("Valor Total", value=data.get('valor_total', ''))
        
        with col3c:
            data['chave_acesso'] = st.text_input("Chave de Acesso", value=data.get('chave_acesso', ''))
            data['natureza_operacao'] = st.text_input("Natureza da Operação", value=data.get('natureza_operacao', ''))
        
        st.session_state.all_extracted_data[selected_file] = data
        
        st.markdown("---")
        st.header("📄 Geração da Capa de Frete")
        
        col_settings1, col_settings2 = st.columns(2)
        
        with col_settings1:
            volume_number = st.text_input(
                "Número do Volume",
                value="1/1",
                help="Formato: volume atual/total de volumes (ex: 1/1, 2/3)"
            )
        
        with col_settings2:
            export_format = st.selectbox(
                "Formato de Exportação",
                options=["PDF", "DOCX"],
                help="Escolha entre PDF ou documento Word"
            )
        
        col_gen1, col_gen2, col_gen3 = st.columns([1, 2, 1])
        
        with col_gen2:
            if st.button("🎯 Gerar Capa de Frete", type="primary", use_container_width=True):
                try:
                    with st.spinner(f"Gerando capa em {export_format}..."):
                        generation_data = data.copy()
                        generation_data['volume_number'] = volume_number
                        
                        if export_format == "PDF":
                            generator = ReceiptGenerator()
                            file_buffer = generator.generate_receipt(generation_data)
                            mime_type = "application/pdf"
                            extension = "pdf"
                        else:
                            generator = DOCXGenerator()
                            file_buffer = generator.generate_receipt(generation_data)
                            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            extension = "docx"
                        
                        if file_buffer:
                            st.success(f"✅ Capa gerada em {export_format} com sucesso!")
                            
                            nf_number = generation_data.get('numero_nfe', 'S_N')
                            loja = generation_data.get('loja', 'S_N')
                            filename = f"Capa_Frete_NF{nf_number}_Loja{loja}.{extension}"
                            
                            st.download_button(
                                label=f"⬇️ Baixar Capa ({export_format})",
                                data=file_buffer,
                                file_name=filename,
                                mime=mime_type,
                                use_container_width=True
                            )
                        else:
                            st.error("❌ Erro ao gerar a capa de frete.")
                            
                except Exception as e:
                    st.error(f"❌ Erro ao gerar capa: {str(e)}")
        
        if len(st.session_state.all_extracted_data) > 1:
            st.markdown("---")
            st.subheader("📦 Geração em Lote")
            
            if st.button(f"🎯 Gerar Todas as Capas ({export_format})", type="secondary", use_container_width=True):
                try:
                    with st.spinner(f"Gerando todas as capas em {export_format}..."):
                        if export_format == "PDF":
                            generator = ReceiptGenerator()
                            mime_type = "application/pdf"
                            extension = "pdf"
                        else:
                            generator = DOCXGenerator()
                            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            extension = "docx"
                        
                        success_count = 0
                        
                        for i, file_data in enumerate(st.session_state.all_extracted_data):
                            generation_data = file_data.copy()
                            generation_data['volume_number'] = volume_number
                            
                            file_buffer = generator.generate_receipt(generation_data)
                            
                            if file_buffer:
                                nf_number = generation_data.get('numero_nfe', f'PDF_{i+1}')
                                loja = generation_data.get('loja', 'S_N')
                                filename = f"Capa_Frete_NF{nf_number}_Loja{loja}.{extension}"
                                
                                st.download_button(
                                    label=f"⬇️ Baixar Capa NF-e {nf_number} ({export_format})",
                                    data=file_buffer,
                                    file_name=filename,
                                    mime=mime_type,
                                    key=f"download_{i}"
                                )
                                success_count += 1
                        
                        st.success(f"✅ {success_count} capas geradas em {export_format} com sucesso!")
                        
                except Exception as e:
                    st.error(f"❌ Erro ao gerar capas: {str(e)}")
    
    else:
        st.info("📤 Faça o upload de arquivos PDF para visualizar os dados extraídos.")

if __name__ == "__main__":
    main()
