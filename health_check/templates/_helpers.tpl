{{- define "health-check.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}
