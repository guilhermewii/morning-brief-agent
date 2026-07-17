# Weekend Agent Challenge: Morning Brief Agent

## Resumo
Morning Brief Agent é um agente serverless que gera um resumo matinal com previsão do tempo, manchetes, agenda e uma frase de motivação. O arquivo é salvo em S3 como `morning_brief_YYYYMMDD.txt` e a execução é agendada diariamente via EventBridge.

## Arquitetura
- **Lambda**: `MorningBriefAgent-Guilherme` (Python 3.10) — gera o conteúdo e grava no S3.  
- **S3**: bucket `meu-morning-brief-guilherme-2026` — armazena os briefs.  
- **EventBridge**: regra/schedule `MorningBriefDailyRule` com `cron(0 9 * * ? *)`.  
- **IAM**: role `MorningBriefLambdaRole-Guilherme` com permissões para CloudWatch Logs e `s3:PutObject` no bucket.

## Fluxo
1. EventBridge dispara a Lambda diariamente às 09:00 UTC.  
2. Lambda gera o texto do briefing e grava `morning_brief_YYYYMMDD.txt` no bucket S3.  
3. (Opcional) Lambda envia e‑mail se variáveis `EMAIL_FROM` e `EMAIL_TO` estiverem configuradas.

## Como testar
- Na console Lambda, clique **Test** para executar manualmente.  
- Verifique CloudWatch Logs para `START/END/REPORT`.  
- Verifique S3 para o arquivo `morning_brief_YYYYMMDD.txt`.

## Evidências
Inclua os screenshots no repositório em `evidencias/`:
- `01_eventbridge_rule.png` — regra/schedule com cron e target.  
- `02_lambda_test.png` — execução da Lambda (succeeded).  
- `03_cloudwatch_report.png` — logs com REPORT e RequestId.  
- `04_s3_list.png` — arquivo no bucket S3.  
- `05_s3_content.png` — conteúdo do arquivo.  
- `06_lambda_permissions.png` — role e policies anexadas.

## Próximos passos recomendados
- Restringir políticas IAM para o mínimo necessário.  
- Adicionar DLQ (SQS) e alarmes CloudWatch para falhas.  
- Automatizar deploy com IaC (CloudFormation / CDK / Terraform).  

## Link do repositório
(https://github.com/guilhermewii/morning-brief-agent)
