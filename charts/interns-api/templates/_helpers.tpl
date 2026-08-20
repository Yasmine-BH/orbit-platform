{{/*
Expand the name of the chart.
*/}}
{{- define "interns-api.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "interns-api.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "interns-api.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels.
*/}}
{{- define "interns-api.labels" -}}
app.kubernetes.io/name: {{ include "interns-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end }}

{{/*
Selector labels.
*/}}
{{- define "interns-api.selectorLabels" -}}
app.kubernetes.io/name: {{ include "interns-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
