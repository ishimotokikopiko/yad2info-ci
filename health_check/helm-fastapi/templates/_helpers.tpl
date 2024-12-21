{{- define "fastapi.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}
