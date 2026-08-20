{{/*
Expand the name of the chart.
*/}}
{{- define "tasks-api.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "tasks-api.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "tasks-api.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels.
*/}}
{{- define "tasks-api.labels" -}}
app.kubernetes.io/name: {{ include "tasks-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end }}

{{/*
Selector labels.
*/}}
{{- define "tasks-api.selectorLabels" -}}
app.kubernetes.io/name: {{ include "tasks-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
