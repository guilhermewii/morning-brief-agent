# Morning Brief Agent

**Descrição**  
Agente serverless que gera um resumo matinal (previsão, manchetes, agenda e motivação) e salva como `morning_brief_YYYYMMDD.txt` em um bucket S3. Agendado via EventBridge.

**Arquivos principais**
- `lambda_function.py` — código da Lambda (Python 3.10)
- `README.md` — instruções do projeto
- `article.md` — texto para publicar no Builder Center
- `evidencias/` — screenshots: `01_eventbridge_rule.png` … `06_lambda_permissions.png`

**Variáveis de ambiente (Lambda)**
- **BUCKET_NAME** — nome do bucket S3 (ex.: `meu-morning-brief-guilherme-2026`)
- **EMAIL_FROM** — (opcional) endereço remetente para envio por e‑mail
- **EMAIL_TO** — (opcional) endereço destinatário para envio por e‑mail
- **REGION** — (opcional) região AWS; padrão `us-east-1`

**Permissões necessárias (mínimo)**
- `AWSLambdaBasicExecutionRole` (CloudWatch Logs)
- Permissão S3 restrita:
  - `s3:PutObject` em `arn:aws:s3:::meu-morning-brief-guilherme-2026/*`
  - `s3:ListBucket` em `arn:aws:s3:::meu-morning-brief-guilherme-2026`
- (Opcional) Permissões SES se for enviar e‑mail: `ses:SendEmail`, `ses:SendRawEmail`

**Deploy rápido (console)**
1. Criar bucket S3 `meu-morning-brief-guilherme-2026`.  
2. Criar role IAM com as permissões mínimas.  
3. Criar Lambda `MorningBriefAgent-Guilherme` (Python 3.10) e anexar a role.  
4. Colar o conteúdo de `lambda_function.py` e salvar.  
5. Criar EventBridge Rule / Scheduler com `cron(0 9 * * ? *)` apontando para a Lambda.  
6. Testar a Lambda manualmente e verificar S3 e CloudWatch.

**Testes**
- Executar **Test** na Lambda → verificar `statusCode: 200` e `s3_key` no output.  
- Verificar CloudWatch Logs por `START/END/REPORT`.  
- Verificar S3 por `morning_brief_YYYYMMDD.txt`.

**Boas práticas**
- Substituir políticas amplas (`AmazonS3FullAccess`, `AmazonSESFullAccess`) por policies restritas.  
- Configurar DLQ (SQS) para invocações que falham.  
- Criar alarme CloudWatch para `Errors` da Lambda.

