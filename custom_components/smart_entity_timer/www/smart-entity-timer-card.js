/*
 * Smart Entity Timer Card
 * Copyright (c) 2026 Abel Smart Timer contributors
 * MIT License
 */

const CARD_VERSION = "1.0.0-rc2";
const MIN_CARD_API_VERSION = 2;
const DOMAIN = "smart_entity_timer";
const ACTION_TURN_ON = "turn_on";
const ACTION_TURN_OFF = "turn_off";
const ACTION_SELECTABLE = "selectable";
const STATUS_ACTIVE = "active";
const STATUS_EXECUTING = "executing";
const STATUS_ERROR = "error";
const RESULT_VISIBLE_MS = 30000;

const I18N = {
  es: {
    card_name: "Temporizador inteligente",
    setup_title: "Configura la tarjeta",
    setup_text: "Selecciona la entidad «Estado del temporizador» creada por Smart Entity Timer.",
    entity_missing: "No se encontró la entidad configurada.",
    incompatible: "La entidad seleccionada no pertenece a una versión compatible de Smart Entity Timer.",
    target_state: "Estado actual",
    action: "Acción al finalizar",
    turn_on: "Encender",
    turn_off: "Apagar",
    duration: "Duración",
    quick_times: "Duraciones rápidas",
    hours: "h",
    minutes: "min",
    seconds: "s",
    decrement: "Restar {value} min",
    increment: "Sumar {value} min",
    remaining: "Tiempo restante",
    programmed: "Tiempo programado",
    idle: "Sin temporizador activo",
    active: "Temporizador activo",
    executing: "Ejecutando acción…",
    restoring: "Restaurando temporizador…",
    error: "Error del temporizador",
    ready_on: "Listo para encender {name}",
    ready_off: "Listo para apagar {name}",
    already_on: "{name} ya está encendido",
    already_off: "{name} ya está apagado",
    unavailable: "{name} no está disponible",
    start: "Iniciar",
    timer_on: "Timer ON",
    cancel: "Cancelar",
    inactive: "Inactivo",
    select_on: "Seleccionar encendido",
    select_off: "Seleccionar apagado",
    open_more_info: "Abrir información de la entidad",
    service_error: "No se pudo completar la operación: {message}",
    api_required: "La tarjeta requiere card_api_version {value} o posterior.",
    last_completed: "Temporizador completado",
    last_cancelled: "Temporizador cancelado",
    last_auto_cancelled: "Cancelado automáticamente: el objetivo se alcanzó antes",
    last_skipped: "Acción omitida por seguridad",
    last_error: "La última operación terminó con error",
    unknown_result: "Última operación actualizada",
    status_on: "Encendido",
    status_off: "Apagado",
    status_unavailable: "No disponible",
    basic_panel: "Configuración general",
    behavior_panel: "Comportamiento",
    visibility_panel: "Secciones visibles",
    colors_panel: "Colores personalizados",
    name: "Nombre personalizado",
    icon: "Icono",
    increment_minutes: "Incremento de los botones",
    layout: "Diseño",
    visual_style: "Estilo visual",
    action_mode: "Acción de la tarjeta",
    progress_style: "Indicador de progreso",
    time_format: "Formato del tiempo",
    quick_times_config: "Duraciones rápidas (minutos)",
    show_header: "Mostrar encabezado",
    show_target_state: "Mostrar estado de la entidad",
    show_action_selector: "Mostrar selector de acción",
    show_duration_controls: "Mostrar controles de duración",
    show_quick_times: "Mostrar duraciones rápidas",
    show_progress: "Mostrar progreso / tiempo",
    show_status: "Mostrar mensaje de estado",
    show_last_result: "Mostrar resultado reciente",
    color_turn_on: "Color Encender",
    color_turn_off: "Color Apagar",
    color_start: "Botón Iniciar",
    color_timer_active: "Botón Timer ON",
    color_cancel: "Botón Cancelar",
    color_inactive: "Botón Inactivo / deshabilitado",
    color_turn_on: "Acción Encender",
    color_turn_off: "Acción Apagar",
    color_progress: "Barra / círculo de progreso",
    color_quick: "Duraciones rápidas",
    color_quick_selected: "Duración rápida seleccionada",
    selectable: "Encender y apagar",
    only_on: "Solo encender",
    only_off: "Solo apagar",
    progress_bar: "Barra",
    progress_ring: "Círculo",
    progress_time: "Solo tiempo",
    time_auto: "Automático",
    time_digital: "Digital",
    time_text: "Texto",
    style_modern: "Moderno",
    style_flat: "Plano",
    style_minimal: "Minimalista",
    layout_auto: "Automático",
    layout_compact: "Compacto",
    layout_expanded: "Expandido",
    layout_mini: "Mini",
    layout_tile: "Mosaico",
    density: "Densidad",
    density_normal: "Normal",
    density_tight: "Ajustada",
    button_mode: "Botones de acción",
    button_auto: "Automático",
    button_inline: "Lado a lado",
    button_primary_only: "Solo acción disponible",
    helper_density: "Si queda vacío, Mini y Mosaico usan densidad ajustada; los demás usan normal.",
    helper_button_mode: "Automático usa botones lado a lado en vistas normales y Mini, y solo la acción disponible en Mosaico.",
    helper_quick_times: "Agrega minutos, por ejemplo 15, 30, 60 y 120. Déjalo vacío para no usar presets.",
    helper_colors: "Cada color controla directamente ese elemento. Si queda vacío, se usa el tema de Home Assistant.",
    helper_action_mode: "Una acción fija oculta el selector y se aplica al iniciar desde esta tarjeta.",
  },
  en: {
    card_name: "Smart Entity Timer",
    setup_title: "Configure the card",
    setup_text: "Select the Timer status entity created by Smart Entity Timer.",
    entity_missing: "The configured entity was not found.",
    incompatible: "The selected entity is not from a compatible Smart Entity Timer version.",
    target_state: "Current state",
    action: "Action at finish",
    turn_on: "Turn on",
    turn_off: "Turn off",
    duration: "Duration",
    quick_times: "Quick durations",
    hours: "h",
    minutes: "min",
    seconds: "s",
    decrement: "Subtract {value} min",
    increment: "Add {value} min",
    remaining: "Time remaining",
    programmed: "Programmed time",
    idle: "No active timer",
    active: "Timer active",
    executing: "Executing action…",
    restoring: "Restoring timer…",
    error: "Timer error",
    ready_on: "Ready to turn on {name}",
    ready_off: "Ready to turn off {name}",
    already_on: "{name} is already on",
    already_off: "{name} is already off",
    unavailable: "{name} is unavailable",
    start: "Start",
    timer_on: "Timer ON",
    cancel: "Cancel",
    inactive: "Inactive",
    select_on: "Select turn on",
    select_off: "Select turn off",
    open_more_info: "Open entity information",
    service_error: "The operation could not be completed: {message}",
    api_required: "The card requires card_api_version {value} or later.",
    last_completed: "Timer completed",
    last_cancelled: "Timer cancelled",
    last_auto_cancelled: "Automatically cancelled: target was reached early",
    last_skipped: "Action skipped for safety",
    last_error: "The last operation ended with an error",
    unknown_result: "Last operation updated",
    status_on: "On",
    status_off: "Off",
    status_unavailable: "Unavailable",
    basic_panel: "General configuration",
    behavior_panel: "Behavior",
    visibility_panel: "Visible sections",
    colors_panel: "Custom colors",
    name: "Custom name",
    icon: "Icon",
    increment_minutes: "Button increment",
    layout: "Layout",
    visual_style: "Visual style",
    action_mode: "Card action",
    progress_style: "Progress indicator",
    time_format: "Time format",
    quick_times_config: "Quick durations (minutes)",
    show_header: "Show header",
    show_target_state: "Show target entity state",
    show_action_selector: "Show action selector",
    show_duration_controls: "Show duration controls",
    show_quick_times: "Show quick durations",
    show_progress: "Show progress / time",
    show_status: "Show status message",
    show_last_result: "Show recent result",
    color_turn_on: "Turn on color",
    color_turn_off: "Turn off color",
    color_start: "Start button",
    color_timer_active: "Timer ON button",
    color_cancel: "Cancel button",
    color_inactive: "Inactive / disabled button",
    color_turn_on: "Turn on action",
    color_turn_off: "Turn off action",
    color_progress: "Progress bar / ring",
    color_quick: "Quick durations",
    color_quick_selected: "Selected quick duration",
    selectable: "Turn on and off",
    only_on: "Turn on only",
    only_off: "Turn off only",
    progress_bar: "Bar",
    progress_ring: "Ring",
    progress_time: "Time only",
    time_auto: "Automatic",
    time_digital: "Digital",
    time_text: "Text",
    style_modern: "Modern",
    style_flat: "Flat",
    style_minimal: "Minimal",
    layout_auto: "Automatic",
    layout_compact: "Compact",
    layout_expanded: "Expanded",
    layout_mini: "Mini",
    layout_tile: "Tile",
    density: "Density",
    density_normal: "Normal",
    density_tight: "Tight",
    button_mode: "Action buttons",
    button_auto: "Automatic",
    button_inline: "Side by side",
    button_primary_only: "Available action only",
    helper_density: "When left empty, Mini and Tile use tight density; other layouts use normal density.",
    helper_button_mode: "Automatic uses side-by-side controls in normal and Mini layouts, and only the available action in Tile.",
    helper_quick_times: "Add minute values such as 15, 30, 60 and 120. Leave empty to disable presets.",
    helper_colors: "Each color directly controls that element. Empty values inherit the Home Assistant theme.",
    helper_action_mode: "A fixed action hides the selector and is applied when starting from this card.",
  },
};

function languageFor(hass) {
  const language = hass?.language || hass?.locale?.language || globalThis.navigator?.language || "en";
  return String(language).toLowerCase().startsWith("es") ? "es" : "en";
}

function t(hass, key, replacements = {}) {
  const language = languageFor(hass);
  let value = I18N[language]?.[key] ?? I18N.en[key] ?? key;
  for (const [name, replacement] of Object.entries(replacements)) {
    value = value.replaceAll(`{${name}}`, String(replacement));
  }
  return value;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function clamp(value, minimum, maximum) {
  return Math.min(maximum, Math.max(minimum, value));
}

function parseDate(value) {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

function formatClock(totalSeconds) {
  const seconds = Math.max(0, Math.ceil(Number(totalSeconds) || 0));
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainder = seconds % 60;
  if (hours > 0) {
    return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}`;
  }
  return `${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}`;
}

function formatMinutes(totalMinutes, hass) {
  const minutes = Math.max(1, Math.round(Number(totalMinutes) || 1));
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  if (hours === 0) return `${remainder} ${t(hass, "minutes")}`;
  if (remainder === 0) return `${hours} ${t(hass, "hours")}`;
  return `${hours} ${t(hass, "hours")} ${remainder} ${t(hass, "minutes")}`;
}

function formatTextSeconds(totalSeconds, hass) {
  const seconds = Math.max(0, Math.ceil(Number(totalSeconds) || 0));
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainder = seconds % 60;
  const parts = [];
  if (hours) parts.push(`${hours} ${t(hass, "hours")}`);
  if (minutes || hours) parts.push(`${minutes} ${t(hass, "minutes")}`);
  parts.push(`${remainder} ${t(hass, "seconds")}`);
  return parts.join(" ");
}

function formatTimeValue(value, mode, hass, active = false) {
  const normalized = ["auto", "digital", "text"].includes(mode) ? mode : "auto";
  if (normalized === "digital") return formatClock(active ? value : Number(value) * 60);
  if (normalized === "text") return active ? formatTextSeconds(value, hass) : formatMinutes(value, hass);
  return active ? formatClock(value) : formatMinutes(value, hass);
}

function parseQuickTimes(value, maximum = 1440) {
  let raw = value;
  if (typeof raw === "string") raw = raw.split(/[,;\s]+/g);
  if (!Array.isArray(raw)) return [];
  const values = [];
  for (const item of raw) {
    const number = Math.round(Number(item));
    if (!Number.isFinite(number) || number < 1 || number > maximum || values.includes(number)) continue;
    values.push(number);
  }
  return values;
}

function normalizeColor(value) {
  if (Array.isArray(value) && value.length === 3) {
    const rgb = value.map((part) => clamp(Math.round(Number(part) || 0), 0, 255));
    return `rgb(${rgb[0]} ${rgb[1]} ${rgb[2]})`;
  }
  if (typeof value !== "string") return undefined;
  const candidate = value.trim();
  if (!candidate) return undefined;
  if (/^#[0-9a-f]{3,8}$/i.test(candidate)) return candidate;
  if (/^(rgb|rgba|hsl|hsla)\([0-9.,%\s/+-]+\)$/i.test(candidate)) return candidate;
  if (/^var\(--[a-z0-9-_]+(?:\s*,\s*[^)]+)?\)$/i.test(candidate)) return candidate;
  if (/^[a-z]+$/i.test(candidate)) return candidate;
  return undefined;
}

function entityDomain(entityId) {
  return String(entityId || "").split(".", 1)[0];
}

function stateIsUsable(state) {
  return Boolean(state && !["unknown", "unavailable"].includes(state));
}

function targetReached(entityId, state, action) {
  if (!stateIsUsable(state)) return false;
  const domain = entityDomain(entityId);
  if (action === ACTION_TURN_OFF) {
    if (domain === "media_player") return ["off", "standby"].includes(state);
    return state === "off";
  }
  if (domain === "media_player") return !["off", "standby"].includes(state);
  if (["climate", "water_heater"].includes(domain)) return state !== "off";
  return state === "on";
}

function statusLabel(hass, state) {
  if (!stateIsUsable(state)) return t(hass, "status_unavailable");
  return state === "off" || state === "standby" ? t(hass, "status_off") : t(hass, "status_on");
}

function option(value, label) {
  return { value, label };
}

class SmartEntityTimerCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = undefined;
    this._config = {};
    this._lastSignature = undefined;
    this._tickInterval = undefined;
    this._resultTimeout = undefined;
    this._resultTimeoutKey = undefined;
    this._pendingReconcileTimeout = undefined;
    this._draftMinutes = 60;
    this._draftAction = ACTION_TURN_OFF;
    this._pendingDuration = undefined;
    this._pendingAction = undefined;
    this._pending = false;
    this._errorMessage = undefined;
  }

  static getStubConfig() {
    return {
      entity: "",
      increment_minutes: 30,
      layout: "auto",
      visual_style: "modern",
      action_mode: "selectable",
      button_mode: "auto",
      progress_style: "bar",
      time_format: "auto",
      quick_times: [],
      show_header: true,
      show_target_state: true,
      show_action_selector: true,
      show_duration_controls: true,
      show_quick_times: true,
      show_progress: true,
      show_status: true,
      show_last_result: true,
    };
  }

  static getConfigForm() {
    const spanish = String(globalThis.navigator?.language || "en").toLowerCase().startsWith("es");
    const dict = I18N[spanish ? "es" : "en"];
    const selectOptions = (entries) => entries.map(([value, label]) => option(value, label));

    return {
      schema: [
        {
          type: "expandable",
          name: "",
          title: dict.basic_panel,
          flatten: true,
          schema: [
            {
              name: "entity",
              required: true,
              selector: { entity: { filter: [{ integration: DOMAIN, domain: "sensor" }] } },
            },
            {
              type: "grid",
              name: "",
              flatten: true,
              column_min_width: "180px",
              schema: [
                { name: "name", selector: { text: {} } },
                { name: "icon", selector: { icon: {} }, context: { icon_entity: "entity" } },
                {
                  name: "layout",
                  selector: {
                    select: {
                      options: selectOptions([
                        ["auto", dict.layout_auto],
                        ["compact", dict.layout_compact],
                        ["expanded", dict.layout_expanded],
                        ["mini", dict.layout_mini],
                        ["tile", dict.layout_tile],
                      ]),
                    },
                  },
                },
                {
                  name: "visual_style",
                  selector: {
                    select: {
                      options: selectOptions([
                        ["modern", dict.style_modern],
                        ["flat", dict.style_flat],
                        ["minimal", dict.style_minimal],
                      ]),
                    },
                  },
                },
                {
                  name: "density",
                  selector: {
                    select: {
                      options: selectOptions([
                        ["normal", dict.density_normal],
                        ["tight", dict.density_tight],
                      ]),
                    },
                  },
                },
              ],
            },
          ],
        },
        {
          type: "expandable",
          name: "",
          title: dict.behavior_panel,
          flatten: true,
          schema: [
            {
              name: "action_mode",
              selector: {
                select: {
                  options: selectOptions([
                    ["selectable", dict.selectable],
                    ["turn_on", dict.only_on],
                    ["turn_off", dict.only_off],
                  ]),
                },
              },
            },
            {
              name: "button_mode",
              selector: {
                select: {
                  options: selectOptions([
                    ["auto", dict.button_auto],
                    ["inline", dict.button_inline],
                    ["primary_only", dict.button_primary_only],
                  ]),
                },
              },
            },
            {
              type: "grid",
              name: "",
              flatten: true,
              column_min_width: "180px",
              schema: [
                {
                  name: "increment_minutes",
                  selector: { number: { min: 1, max: 1440, step: 1, mode: "box", unit_of_measurement: "min" } },
                },
                {
                  name: "progress_style",
                  selector: {
                    select: {
                      options: selectOptions([
                        ["bar", dict.progress_bar],
                        ["ring", dict.progress_ring],
                        ["time", dict.progress_time],
                      ]),
                    },
                  },
                },
                {
                  name: "time_format",
                  selector: {
                    select: {
                      options: selectOptions([
                        ["auto", dict.time_auto],
                        ["digital", dict.time_digital],
                        ["text", dict.time_text],
                      ]),
                    },
                  },
                },
              ],
            },
            { name: "quick_times", selector: { text: { multiple: true } } },
          ],
        },
        {
          type: "expandable",
          name: "",
          title: dict.visibility_panel,
          flatten: true,
          schema: [
            {
              type: "grid",
              name: "",
              flatten: true,
              column_min_width: "180px",
              schema: [
                { name: "show_header", selector: { boolean: {} } },
                { name: "show_target_state", selector: { boolean: {} } },
                { name: "show_action_selector", selector: { boolean: {} } },
                { name: "show_duration_controls", selector: { boolean: {} } },
                { name: "show_quick_times", selector: { boolean: {} } },
                { name: "show_progress", selector: { boolean: {} } },
                { name: "show_status", selector: { boolean: {} } },
                { name: "show_last_result", selector: { boolean: {} } },
              ],
            },
          ],
        },
        {
          type: "expandable",
          name: "",
          title: dict.colors_panel,
          flatten: true,
          schema: [
            {
              type: "grid",
              name: "",
              flatten: true,
              column_min_width: "180px",
              schema: [
                { name: "color_start", selector: { color_rgb: {} } },
                { name: "color_timer_active", selector: { color_rgb: {} } },
                { name: "color_cancel", selector: { color_rgb: {} } },
                { name: "color_inactive", selector: { color_rgb: {} } },
                { name: "color_turn_on", selector: { color_rgb: {} } },
                { name: "color_turn_off", selector: { color_rgb: {} } },
                { name: "color_progress", selector: { color_rgb: {} } },
                { name: "color_quick", selector: { color_rgb: {} } },
                { name: "color_quick_selected", selector: { color_rgb: {} } },
              ],
            },
          ],
        },
      ],
      computeLabel: (schema) => dict[schema.name] || schema.name,
      computeHelper: (schema) => {
        if (schema.name === "entity") {
          return spanish
            ? "Selecciona el sensor Estado del temporizador de Smart Entity Timer 0.1.3 o posterior."
            : "Select the Timer status sensor from Smart Entity Timer 0.1.3 or later.";
        }
        if (schema.name === "increment_minutes") {
          return spanish
            ? "Valor usado por los botones − y +. Puedes introducir cualquier duración manualmente."
            : "Used by the − and + buttons. Any duration can still be entered manually.";
        }
        if (schema.name === "quick_times") return dict.helper_quick_times;
        if (schema.name === "action_mode") return dict.helper_action_mode;
        if (schema.name === "button_mode") return dict.helper_button_mode;
        if (schema.name === "density") return dict.helper_density;
        if (schema.name?.startsWith("color_")) return dict.helper_colors;
        return undefined;
      },
      assertConfig: (config) => {
        if (config.entity && entityDomain(config.entity) !== "sensor") {
          throw new Error(spanish ? "La entidad principal debe ser un sensor." : "The main entity must be a sensor.");
        }
      },
    };
  }

  setConfig(config) {
    if (!config || typeof config !== "object") throw new Error("Invalid Smart Entity Timer Card configuration");
    const previousEntity = this._config?.entity;
    this._rawConfig = { ...config };
    this._config = {
      increment_minutes: 30,
      layout: "auto",
      visual_style: "modern",
      action_mode: "selectable",
      button_mode: "auto",
      progress_style: "bar",
      time_format: "auto",
      quick_times: [],
      show_header: true,
      show_target_state: true,
      show_action_selector: true,
      show_duration_controls: true,
      show_quick_times: true,
      show_progress: true,
      show_status: true,
      show_last_result: true,
      ...config,
    };
    if (previousEntity !== this._config.entity) {
      this._lastSignature = undefined;
      this._pendingDuration = undefined;
      this._pendingAction = undefined;
    }
    this._syncDrafts();
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._reconcilePending();
    this._syncDrafts();
    this._updateTicking();
    this._scheduleResultExpiry();
    const signature = this._relevantSignature();
    if (signature !== this._lastSignature) {
      this._lastSignature = signature;
      this._render();
    }
  }

  get hass() {
    return this._hass;
  }

  connectedCallback() {
    this._render();
    this._updateTicking();
  }

  disconnectedCallback() {
    this._clearTicking();
    if (this._resultTimeout) clearTimeout(this._resultTimeout);
    this._resultTimeout = undefined;
    if (this._pendingReconcileTimeout) clearTimeout(this._pendingReconcileTimeout);
    this._pendingReconcileTimeout = undefined;
  }

  getCardSize() {
    const layout = this._config.layout;
    if (layout === "tile") return 2;
    if (layout === "mini") return 3;
    if (layout === "compact") return this._config.visual_style === "minimal" ? 4 : 5;
    return this._config.visual_style === "minimal" ? 5 : 6;
  }

  getGridOptions() {
    const layout = this._config.layout;
    let rows = this._config.visual_style === "minimal" ? 5 : 6;
    if (layout === "compact") rows = this._config.visual_style === "minimal" ? 4 : 5;
    if (layout === "mini") rows = 3;
    if (layout === "tile") rows = 2;
    return {
      rows,
      columns: 6,
      min_rows: layout === "tile" ? 2 : 3,
      min_columns: 3,
    };
  }

  _hasExplicitConfig(name) {
    return Object.prototype.hasOwnProperty.call(this._rawConfig || {}, name);
  }

  _effectiveDensity(layout) {
    if (["normal", "tight"].includes(this._config.density)) return this._config.density;
    return ["mini", "tile"].includes(layout) ? "tight" : "normal";
  }

  _effectiveButtonMode(layout) {
    const configured = ["auto", "inline", "primary_only"].includes(this._config.button_mode)
      ? this._config.button_mode
      : "auto";
    if (configured !== "auto") return configured;
    return layout === "tile" ? "primary_only" : "inline";
  }

  _effectiveVisibility(name, layout, active) {
    // A user can always hide a section. Mini/Tile additionally impose
    // structural hiding so switching an existing 0.2.x card to a compact
    // layout works even when old YAML contains explicit show_*: true values.
    if (!this._config[name]) return false;

    if (layout === "mini") {
      if (name === "show_target_state") return false;
      if (active && ["show_action_selector", "show_duration_controls", "show_quick_times"].includes(name)) return false;
      return true;
    }

    if (layout === "tile") {
      if (["show_target_state", "show_quick_times", "show_status", "show_last_result"].includes(name)) return false;
      if (!active && name === "show_progress") return false;
      if (active && ["show_action_selector", "show_duration_controls"].includes(name)) return false;
      return true;
    }

    return true;
  }

  _statusState() {
    return this._hass?.states?.[this._config.entity];
  }

  _relevantSignature() {
    if (!this._hass) return "no-hass";
    const state = this._statusState();
    return `${this._config.entity}:${state?.state ?? "missing"}:${state?.last_updated ?? ""}:${state?.last_changed ?? ""}`;
  }

  _backendDuration() {
    const minutes = Number(this._statusState()?.attributes?.duration_minutes);
    return Number.isFinite(minutes) && minutes >= 1 ? Math.round(minutes) : undefined;
  }

  _backendAction() {
    const action = this._statusState()?.attributes?.end_action;
    return [ACTION_TURN_ON, ACTION_TURN_OFF].includes(action) ? action : undefined;
  }

  _fixedAction() {
    return [ACTION_TURN_ON, ACTION_TURN_OFF].includes(this._config.action_mode) ? this._config.action_mode : undefined;
  }

  _idleAction() {
    return this._fixedAction() || this._draftAction;
  }

  _reconcilePending() {
    const status = this._statusState();
    if (!status) return;
    const now = Date.now();
    const lastUpdated = status.last_updated || status.last_changed || "";

    if (this._pendingDuration) {
      const backend = this._backendDuration();
      const changed = lastUpdated && lastUpdated !== this._pendingDuration.baseline;
      const expired = now - this._pendingDuration.started > 2500;
      if (backend === this._pendingDuration.value || changed || expired) this._pendingDuration = undefined;
    }

    if (this._pendingAction) {
      const backend = this._backendAction();
      const changed = lastUpdated && lastUpdated !== this._pendingAction.baseline;
      const expired = now - this._pendingAction.started > 2500;
      if (backend === this._pendingAction.value || changed || expired) this._pendingAction = undefined;
    }
  }

  _schedulePendingReconcile() {
    if (this._pendingReconcileTimeout) clearTimeout(this._pendingReconcileTimeout);
    this._pendingReconcileTimeout = setTimeout(() => {
      this._pendingReconcileTimeout = undefined;
      this._reconcilePending();
      this._syncDrafts();
      this._render();
    }, 2600);
  }

  _syncDrafts() {
    const status = this._statusState();
    if (!status) return;
    const busy = [STATUS_ACTIVE, STATUS_EXECUTING].includes(status.state);
    const backendDuration = this._backendDuration();
    const backendAction = this._backendAction();

    if (!this._pendingDuration || busy) {
      if (backendDuration !== undefined) this._draftMinutes = backendDuration;
      if (busy) this._pendingDuration = undefined;
    } else {
      this._draftMinutes = this._pendingDuration.value;
    }

    if (!this._pendingAction || busy) {
      if (backendAction !== undefined) this._draftAction = backendAction;
      if (busy) this._pendingAction = undefined;
    } else {
      this._draftAction = this._pendingAction.value;
    }
  }

  _maxDuration() {
    const constraints = this._statusState()?.attributes?.constraints;
    const maxSeconds = Number(constraints?.max_seconds);
    if (Number.isFinite(maxSeconds) && maxSeconds >= 60) return Math.max(1, Math.floor(maxSeconds / 60));
    return 1440;
  }

  _remainingAndProgress() {
    const status = this._statusState();
    const startedAt = parseDate(status?.attributes?.started_at);
    const finishesAt = parseDate(status?.attributes?.finishes_at);
    if (!finishesAt) {
      return { remaining: Number(status?.attributes?.remaining_seconds_snapshot) || 0, progress: 0 };
    }
    const now = Date.now();
    const remaining = Math.max(0, Math.ceil((finishesAt.getTime() - now) / 1000));
    const total = startedAt
      ? Math.max(1, (finishesAt.getTime() - startedAt.getTime()) / 1000)
      : Math.max(1, Number(status?.attributes?.duration_seconds) || this._draftMinutes * 60);
    const elapsed = clamp(total - remaining, 0, total);
    return { remaining, progress: clamp((elapsed / total) * 100, 0, 100) };
  }

  _localCanStart() {
    const status = this._statusState();
    if (!status || [STATUS_ACTIVE, STATUS_EXECUTING].includes(status.state)) return false;
    if (this._pending) return false;
    const targetState = status.attributes.target_entity_state;
    const targetEntity = status.attributes.target_entity;
    const action = this._idleAction();
    if (!stateIsUsable(targetState)) return false;
    if (targetReached(targetEntity, targetState, action)) return false;
    return this._draftMinutes >= 1 && this._draftMinutes <= this._maxDuration();
  }

  _quickDurations() {
    return parseQuickTimes(this._config.quick_times, this._maxDuration());
  }

  _updateTicking() {
    const status = this._statusState()?.state;
    const shouldTick = [STATUS_ACTIVE, STATUS_EXECUTING].includes(status);
    if (shouldTick && !this._tickInterval) this._tickInterval = setInterval(() => this._render(), 1000);
    else if (!shouldTick) this._clearTicking();
  }

  _clearTicking() {
    if (this._tickInterval) clearInterval(this._tickInterval);
    this._tickInterval = undefined;
  }

  _scheduleResultExpiry() {
    const lastFinished = this._statusState()?.attributes?.last_finished_at;
    if (!lastFinished || lastFinished === this._resultTimeoutKey) return;
    this._resultTimeoutKey = lastFinished;
    if (this._resultTimeout) clearTimeout(this._resultTimeout);
    const date = parseDate(lastFinished);
    if (!date) return;
    const delay = Math.max(0, date.getTime() + RESULT_VISIBLE_MS - Date.now());
    this._resultTimeout = setTimeout(() => this._render(), delay + 50);
  }

  _recentResult() {
    if (!this._config.show_last_result) return undefined;
    const status = this._statusState();
    const finished = parseDate(status?.attributes?.last_finished_at);
    if (!finished || Date.now() - finished.getTime() > RESULT_VISIBLE_MS) return undefined;
    const result = status.attributes.last_result;
    const keys = {
      completed: "last_completed",
      cancelled: "last_cancelled",
      auto_cancelled: "last_auto_cancelled",
      skipped: "last_skipped",
      error: "last_error",
    };
    return {
      label: t(this._hass, keys[result] || "unknown_result"),
      message: status.attributes.last_message,
      type: result === "error" ? "error" : result === "completed" ? "success" : "info",
    };
  }

  _statusMessage(status, targetName, targetState, targetEntity, action) {
    if (this._errorMessage) return { type: "error", text: this._errorMessage };
    if (status.attributes.restore_pending) return { type: "info", text: t(this._hass, "restoring") };
    if (status.state === STATUS_EXECUTING) return { type: "info", text: t(this._hass, "executing") };
    if (status.state === STATUS_ERROR) return { type: "error", text: status.attributes.last_message || t(this._hass, "error") };
    if (status.state === STATUS_ACTIVE) return { type: "active", text: t(this._hass, "active") };

    const recent = this._recentResult();
    if (recent) return { type: recent.type, text: recent.message || recent.label, label: recent.label };
    if (!stateIsUsable(targetState)) return { type: "warning", text: t(this._hass, "unavailable", { name: targetName }) };
    if (targetReached(targetEntity, targetState, action)) {
      return {
        type: "muted",
        text: t(this._hass, action === ACTION_TURN_ON ? "already_on" : "already_off", { name: targetName }),
      };
    }
    return {
      type: "ready",
      text: t(this._hass, action === ACTION_TURN_ON ? "ready_on" : "ready_off", { name: targetName }),
    };
  }

  _colorVariables() {
    const entries = [
      ["--set-custom-on", normalizeColor(this._config.color_turn_on)],
      ["--set-custom-off", normalizeColor(this._config.color_turn_off)],
      ["--set-custom-start", normalizeColor(this._config.color_start)],
      ["--set-custom-timer-active", normalizeColor(this._config.color_timer_active)],
      ["--set-custom-cancel", normalizeColor(this._config.color_cancel)],
      ["--set-custom-inactive", normalizeColor(this._config.color_inactive)],
      ["--set-custom-progress", normalizeColor(this._config.color_progress)],
      ["--set-custom-quick", normalizeColor(this._config.color_quick)],
      ["--set-custom-quick-selected", normalizeColor(this._config.color_quick_selected)],
    ];
    return entries.filter(([, value]) => value).map(([name, value]) => `${name}:${value}`).join(";");
  }

  _renderProgress(style, active, progress, value, label, visible = this._config.show_progress) {
    if (!visible) return "";
    const safeProgress = active ? clamp(progress, 0, 100) : 0;
    if (style === "ring") {
      return `
        <div class="progress-visual ring-mode">
          <div class="ring-wrap" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${escapeHtml(Math.round(safeProgress))}">
            <svg viewBox="0 0 120 120" aria-hidden="true">
              <circle class="ring-track" cx="60" cy="60" r="50"></circle>
              <circle class="ring-value" cx="60" cy="60" r="50" pathLength="100" style="stroke-dasharray:${escapeHtml(safeProgress)} 100"></circle>
            </svg>
            <div class="ring-center"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(label)}</span></div>
          </div>
        </div>`;
    }
    if (style === "time") {
      return `
        <div class="progress-visual time-mode">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(value)}</strong>
        </div>`;
    }
    return `
      <div class="progress-visual bar-mode">
        <div class="progress-heading"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>
        <div class="progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${escapeHtml(Math.round(safeProgress))}">
          <div class="progress-fill" style="width:${escapeHtml(safeProgress)}%"></div>
        </div>
      </div>`;
  }

  _render() {
    if (!this.shadowRoot) return;
    if (!this._config.entity) {
      this.shadowRoot.innerHTML = `${this._styles()}<ha-card><div class="setup"><div class="setup-icon">⏱</div><strong>${escapeHtml(t(this._hass, "setup_title"))}</strong><span>${escapeHtml(t(this._hass, "setup_text"))}</span></div></ha-card>`;
      return;
    }
    if (!this._hass) {
      this.shadowRoot.innerHTML = `${this._styles()}<ha-card><div class="setup"><div class="spinner"></div></div></ha-card>`;
      return;
    }
    const status = this._statusState();
    if (!status) {
      this.shadowRoot.innerHTML = `${this._styles()}<ha-card><div class="setup error-panel"><strong>${escapeHtml(t(this._hass, "entity_missing"))}</strong><code>${escapeHtml(this._config.entity)}</code></div></ha-card>`;
      return;
    }

    const apiVersion = Number(status.attributes.card_api_version);
    if (!Number.isFinite(apiVersion) || apiVersion < MIN_CARD_API_VERSION) {
      this.shadowRoot.innerHTML = `${this._styles()}<ha-card><div class="setup error-panel"><strong>${escapeHtml(t(this._hass, "incompatible"))}</strong><span>${escapeHtml(t(this._hass, "api_required", { value: MIN_CARD_API_VERSION }))}</span></div></ha-card>`;
      return;
    }

    this._syncDrafts();
    this._updateTicking();
    this._scheduleResultExpiry();

    const active = status.state === STATUS_ACTIVE;
    const executing = status.state === STATUS_EXECUTING;
    const busy = active || executing;
    const action = busy ? status.attributes.end_action : this._idleAction();
    const targetName = status.attributes.target_entity_name || status.attributes.target_entity || this._config.entity;
    const targetEntity = status.attributes.target_entity;
    const targetState = status.attributes.target_entity_state;
    const title = this._config.name || targetName || t(this._hass, "card_name");
    const icon = this._config.icon || (action === ACTION_TURN_ON ? "mdi:timer-play-outline" : "mdi:timer-off-outline");
    const increment = clamp(Math.round(Number(this._config.increment_minutes) || 30), 1, 1440);
    const maxDuration = this._maxDuration();
    const displayMinutes = busy ? Number(status.attributes.duration_minutes) || this._draftMinutes : this._draftMinutes;
    const hours = Math.floor(displayMinutes / 60);
    const minutes = displayMinutes % 60;
    const { remaining, progress } = this._remainingAndProgress();
    const canStart = this._localCanStart();
    const canCancel = active && !this._pending;
    const statusMessage = this._statusMessage(status, targetName, targetState, targetEntity, action);
    const layoutClass = ["compact", "expanded", "mini", "tile"].includes(this._config.layout) ? this._config.layout : "auto";
    const visualStyle = ["flat", "minimal"].includes(this._config.visual_style) ? this._config.visual_style : "modern";
    const progressStyle = ["ring", "time"].includes(this._config.progress_style) ? this._config.progress_style : "bar";
    const timeFormat = ["digital", "text"].includes(this._config.time_format) ? this._config.time_format : "auto";
    const actionLabel = action === ACTION_TURN_ON ? t(this._hass, "turn_on") : t(this._hass, "turn_off");
    const progressLabel = active ? t(this._hass, "remaining") : t(this._hass, "programmed");
    const progressValue = formatTimeValue(active ? remaining : displayMinutes, timeFormat, this._hass, active);
    const quickTimes = this._quickDurations();
    const fixedAction = this._fixedAction();
    const showHeader = this._effectiveVisibility("show_header", layoutClass, active);
    const showTargetState = this._effectiveVisibility("show_target_state", layoutClass, active);
    const showActionSelector = this._effectiveVisibility("show_action_selector", layoutClass, active);
    const showDurationControls = this._effectiveVisibility("show_duration_controls", layoutClass, active);
    const showQuickTimes = this._effectiveVisibility("show_quick_times", layoutClass, active);
    const showProgress = this._effectiveVisibility("show_progress", layoutClass, active);
    const showStatus = this._effectiveVisibility("show_status", layoutClass, active);
    const showAction = showActionSelector && !fixedAction;
    const density = this._effectiveDensity(layoutClass);
    const buttonMode = this._effectiveButtonMode(layoutClass);
    const customVars = this._colorVariables();

    const header = showHeader ? `
      <header>
        <button class="entity-icon" id="more-info" title="${escapeHtml(t(this._hass, "open_more_info"))}" aria-label="${escapeHtml(t(this._hass, "open_more_info"))}">
          <ha-icon icon="${escapeHtml(icon)}"></ha-icon>
        </button>
        <div class="heading">
          <div class="title">${escapeHtml(title)}</div>
          <div class="subtitle">${escapeHtml(targetName)}</div>
        </div>
        <div class="action-badge"><span class="badge-dot"></span>${escapeHtml(actionLabel)}</div>
      </header>` : "";

    const targetSection = showTargetState ? `
      <button class="target-state" id="target-more-info" aria-label="${escapeHtml(t(this._hass, "open_more_info"))}">
        <span>${escapeHtml(t(this._hass, "target_state"))}</span>
        <strong>${escapeHtml(statusLabel(this._hass, targetState))}</strong>
        <span class="raw-state">${escapeHtml(targetState ?? "unavailable")}</span>
      </button>` : "";

    const actionSection = showAction ? `
      <section class="action-section">
        <div class="section-label">${escapeHtml(t(this._hass, "action"))}</div>
        <div class="segmented" role="group" aria-label="${escapeHtml(t(this._hass, "action"))}">
          <button id="turn-on" class="segment segment-on ${action === ACTION_TURN_ON ? "selected" : ""}" ${busy || this._pending ? "disabled" : ""} aria-label="${escapeHtml(t(this._hass, "select_on"))}">
            <ha-icon icon="mdi:power-plug-outline"></ha-icon><span>${escapeHtml(t(this._hass, "turn_on"))}</span>
          </button>
          <button id="turn-off" class="segment segment-off ${action === ACTION_TURN_OFF ? "selected" : ""}" ${busy || this._pending ? "disabled" : ""} aria-label="${escapeHtml(t(this._hass, "select_off"))}">
            <ha-icon icon="mdi:power-plug-off-outline"></ha-icon><span>${escapeHtml(t(this._hass, "turn_off"))}</span>
          </button>
        </div>
      </section>` : "";

    const durationSection = showDurationControls ? `
      <section class="duration-section">
        <div class="section-label">${escapeHtml(t(this._hass, "duration"))}</div>
        <div class="duration-control">
          <button id="decrement" class="step-button" ${busy || this._pending || displayMinutes <= 1 ? "disabled" : ""} aria-label="${escapeHtml(t(this._hass, "decrement", { value: increment }))}">
            <ha-icon icon="mdi:minus"></ha-icon><span>${escapeHtml(increment)} min</span>
          </button>
          <div class="time-inputs ${busy ? "locked" : ""}">
            <label><input id="hours" type="number" inputmode="numeric" min="0" max="168" value="${escapeHtml(hours)}" ${busy || this._pending ? "disabled" : ""}><span>${escapeHtml(t(this._hass, "hours"))}</span></label>
            <div class="time-separator">:</div>
            <label><input id="minutes" type="number" inputmode="numeric" min="0" max="59" value="${escapeHtml(minutes)}" ${busy || this._pending ? "disabled" : ""}><span>${escapeHtml(t(this._hass, "minutes"))}</span></label>
          </div>
          <button id="increment" class="step-button" ${busy || this._pending || displayMinutes >= maxDuration ? "disabled" : ""} aria-label="${escapeHtml(t(this._hass, "increment", { value: increment }))}">
            <ha-icon icon="mdi:plus"></ha-icon><span>${escapeHtml(increment)} min</span>
          </button>
        </div>
      </section>` : "";

    const quickSection = showQuickTimes && quickTimes.length ? `
      <section class="quick-section">
        <div class="section-label">${escapeHtml(t(this._hass, "quick_times"))}</div>
        <div class="quick-grid">
          ${quickTimes.map((value) => `<button class="quick-button ${!busy && displayMinutes === value ? "selected" : ""}" data-quick-minutes="${escapeHtml(value)}" ${busy || this._pending ? "disabled" : ""}>${escapeHtml(formatMinutes(value, this._hass))}</button>`).join("")}
        </div>
      </section>` : "";

    const progressVisual = this._renderProgress(progressStyle, active, progress, progressValue, progressLabel, showProgress);
    const statusBlock = showStatus ? `
      <div class="status-message ${escapeHtml(statusMessage.type)}">
        <span class="status-indicator"></span>
        <div><strong>${escapeHtml(statusMessage.label || (active ? t(this._hass, "active") : t(this._hass, "idle")))}</strong><span>${escapeHtml(statusMessage.text)}</span></div>
      </div>` : "";
    const progressSection = progressVisual || statusBlock ? `<section class="progress-section">${progressVisual}${statusBlock}</section>` : "";

    const startStateClass = active || executing ? "timer-active" : canStart ? "start-ready" : "start-disabled";
    const cancelStateClass = canCancel ? "cancel-ready" : "inactive-state";
    const startButton = `
        <button id="start" class="primary-action ${startStateClass}" ${canStart ? "" : "disabled"}>
          <ha-icon icon="${active || executing ? "mdi:timer-sand" : "mdi:play"}"></ha-icon>
          <span>${escapeHtml(active || executing ? t(this._hass, "timer_on") : t(this._hass, "start"))}</span>
        </button>`;
    const cancelButton = `
        <button id="cancel" class="cancel-action ${cancelStateClass}" ${canCancel ? "" : "disabled"}>
          <ha-icon icon="${canCancel ? "mdi:close-circle-outline" : "mdi:timer-off-outline"}"></ha-icon>
          <span>${escapeHtml(canCancel ? t(this._hass, "cancel") : t(this._hass, "inactive"))}</span>
        </button>`;

    let footerButtons = `${startButton}${cancelButton}`;
    if (buttonMode === "primary_only") {
      if (active && canCancel) footerButtons = cancelButton;
      else if (active || executing) footerButtons = startButton;
      else footerButtons = startButton;
    }
    const footer = `<footer class="buttons-${escapeHtml(buttonMode)}">${footerButtons}</footer>`;

    this.shadowRoot.innerHTML = `
      ${this._styles()}
      <ha-card style="${escapeHtml(customVars)}" class="timer-card ${layoutClass} density-${density} buttons-${buttonMode} style-${visualStyle} progress-${progressStyle} action-${escapeHtml(action)} status-${escapeHtml(status.state)}">
        <div class="accent"></div>
        <div class="content">${header}${targetSection}${actionSection}${durationSection}${quickSection}${progressSection}${footer}</div>
      </ha-card>`;

    this._bindEvents();
  }

  _bindEvents() {
    const byId = (id) => this.shadowRoot?.getElementById(id);
    byId("more-info")?.addEventListener("click", () => this._showMoreInfo());
    byId("target-more-info")?.addEventListener("click", () => this._showMoreInfo());
    byId("turn-on")?.addEventListener("click", () => this._setAction(ACTION_TURN_ON));
    byId("turn-off")?.addEventListener("click", () => this._setAction(ACTION_TURN_OFF));
    byId("decrement")?.addEventListener("click", () => this._adjustDuration(-1));
    byId("increment")?.addEventListener("click", () => this._adjustDuration(1));
    byId("start")?.addEventListener("click", () => this._start());
    byId("cancel")?.addEventListener("click", () => this._cancel());
    this.shadowRoot?.querySelectorAll?.("[data-quick-minutes]")?.forEach((button) => {
      button.addEventListener("click", () => this._setDuration(Number(button.dataset.quickMinutes)));
    });

    const hours = byId("hours");
    const minutes = byId("minutes");
    const updateDraft = () => {
      const total = Math.max(1, (Number(hours?.value) || 0) * 60 + (Number(minutes?.value) || 0));
      this._draftMinutes = clamp(Math.round(total), 1, this._maxDuration());
    };
    const commit = () => {
      updateDraft();
      this._setDuration(this._draftMinutes);
    };
    hours?.addEventListener("input", updateDraft);
    minutes?.addEventListener("input", updateDraft);
    hours?.addEventListener("change", commit);
    minutes?.addEventListener("change", commit);
  }

  _showMoreInfo() {
    const entityId = this._statusState()?.attributes?.target_entity;
    if (!entityId) return;
    this.dispatchEvent(new CustomEvent("hass-more-info", { bubbles: true, composed: true, detail: { entityId } }));
  }

  async _setAction(action) {
    if (![ACTION_TURN_ON, ACTION_TURN_OFF].includes(action) || this._fixedAction()) return;
    const status = this._statusState();
    const baseline = status?.last_updated || status?.last_changed || "";
    this._draftAction = action;
    this._pendingAction = { value: action, baseline, started: Date.now() };
    this._pending = true;
    this._errorMessage = undefined;
    this._render();
    try {
      await this._hass.callService(DOMAIN, "set_values", { entity_id: this._config.entity, end_action: action });
    } catch (error) {
      this._pendingAction = undefined;
      this._showServiceError(error);
    } finally {
      this._pending = false;
      this._reconcilePending();
      this._schedulePendingReconcile();
      this._syncDrafts();
      this._render();
    }
  }

  async _setDuration(minutes) {
    const value = clamp(Math.round(minutes), 1, this._maxDuration());
    const status = this._statusState();
    const baseline = status?.last_updated || status?.last_changed || "";
    this._draftMinutes = value;
    this._pendingDuration = { value, baseline, started: Date.now() };
    this._pending = true;
    this._errorMessage = undefined;
    this._render();
    try {
      await this._hass.callService(DOMAIN, "set_values", { entity_id: this._config.entity, duration_minutes: value });
    } catch (error) {
      this._pendingDuration = undefined;
      this._showServiceError(error);
    } finally {
      this._pending = false;
      this._reconcilePending();
      this._schedulePendingReconcile();
      this._syncDrafts();
      this._render();
    }
  }

  _adjustDuration(direction) {
    const increment = clamp(Math.round(Number(this._config.increment_minutes) || 30), 1, 1440);
    this._setDuration(this._draftMinutes + direction * increment);
  }

  async _start() {
    if (!this._localCanStart()) return;
    this._pending = true;
    this._errorMessage = undefined;
    this._render();
    try {
      const fixedAction = this._fixedAction();
      if (fixedAction && this._backendAction() !== fixedAction) {
        await this._hass.callService(DOMAIN, "set_values", { entity_id: this._config.entity, end_action: fixedAction });
      }
      await this._hass.callService(DOMAIN, "start", { entity_id: this._config.entity });
    } catch (error) {
      this._showServiceError(error);
    } finally {
      this._pending = false;
      this._render();
    }
  }

  async _cancel() {
    const status = this._statusState();
    if (status?.state !== STATUS_ACTIVE) return;
    this._pending = true;
    this._errorMessage = undefined;
    this._render();
    try {
      await this._hass.callService(DOMAIN, "cancel", { entity_id: this._config.entity });
    } catch (error) {
      this._showServiceError(error);
    } finally {
      this._pending = false;
      this._render();
    }
  }

  _showServiceError(error) {
    const message = error?.message || String(error || "unknown error");
    this._errorMessage = t(this._hass, "service_error", { message });
    console.error("Smart Entity Timer Card service error", error);
    this._render();
  }

  _styles() {
    return `<style>
      :host {
        display: block;
        container-type: inline-size;
      }
      .timer-card {
        /*
         * Custom colors are written inline on this ha-card element.
         * Resolve all derived variables at the same scope so values chosen
         * in the visual editor are visible to the complete card subtree.
         */
        --set-accent-on: var(--set-custom-on, var(--success-color, #2eaf68));
        --set-accent-off: var(--set-custom-off, var(--warning-color, #e8843d));
        --set-accent: var(--set-accent-off);
        --set-start-color: var(--set-custom-start, var(--set-accent));
        --set-timer-active-color: var(--set-custom-timer-active, var(--primary-color, var(--set-accent)));
        --set-cancel-color: var(--set-custom-cancel, var(--error-color, #db4437));
        --set-inactive-color: var(--set-custom-inactive, var(--secondary-text-color));
        --set-progress-color: var(--set-custom-progress, var(--set-accent));
        --set-quick-color: var(--set-custom-quick, var(--primary-text-color));
        --set-quick-selected-color: var(--set-custom-quick-selected, var(--set-accent));
        --set-surface: color-mix(in srgb, var(--primary-text-color) 5%, transparent);
        --set-border: color-mix(in srgb, var(--primary-text-color) 12%, transparent);
        --set-muted: var(--secondary-text-color);
      }
      * { box-sizing: border-box; }
      ha-card {
        position: relative; overflow: hidden; color: var(--primary-text-color);
        background: var(--ha-card-background, var(--card-background-color));
        border-radius: var(--ha-card-border-radius, 16px);
        border: var(--ha-card-border-width, 0) solid var(--ha-card-border-color, transparent);
      }
      .action-turn_on { --set-accent: var(--set-accent-on); }
      .action-turn_off { --set-accent: var(--set-accent-off); }
      .accent { height: 4px; background: linear-gradient(90deg, var(--set-accent), var(--set-progress-color)); }
      .content { display: grid; gap: 16px; padding: 18px; }
      header { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 12px; }
      .entity-icon {
        width: 46px; height: 46px; border: 0; border-radius: 14px; cursor: pointer; color: var(--set-accent);
        background: color-mix(in srgb, var(--set-accent) 13%, transparent); display: grid; place-items: center;
      }
      .entity-icon ha-icon { --mdc-icon-size: 27px; }
      .heading { min-width: 0; }
      .title { font-size: 1.13rem; line-height: 1.25; font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .subtitle { margin-top: 3px; color: var(--set-muted); font-size: .84rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .action-badge {
        display: inline-flex; align-items: center; gap: 7px; padding: 7px 10px; border-radius: 999px;
        background: color-mix(in srgb, var(--set-accent) 14%, transparent); color: var(--set-accent);
        font-size: .75rem; font-weight: 750; text-transform: uppercase; letter-spacing: .04em;
      }
      .badge-dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; box-shadow: 0 0 0 4px color-mix(in srgb, currentColor 14%, transparent); }
      .target-state {
        width: 100%; border: 1px solid var(--set-border); border-radius: 12px; background: var(--set-surface);
        color: inherit; cursor: pointer; padding: 10px 12px; display: grid; grid-template-columns: 1fr auto auto; gap: 10px; align-items: center; text-align: left;
      }
      .target-state > span:first-child { color: var(--set-muted); font-size: .8rem; }
      .target-state strong { font-size: .83rem; }
      .raw-state { color: var(--set-muted); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .72rem; padding: 3px 6px; border-radius: 6px; background: color-mix(in srgb, var(--primary-text-color) 7%, transparent); }
      section { display: grid; gap: 8px; }
      .section-label { color: var(--set-muted); font-size: .78rem; font-weight: 650; letter-spacing: .02em; }
      .segmented { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 5px; border-radius: 14px; background: var(--set-surface); border: 1px solid var(--set-border); }
      .segment {
        border: 1px solid transparent; min-height: 44px; border-radius: 10px; background: transparent; color: var(--set-muted); cursor: pointer;
        display: flex; align-items: center; justify-content: center; gap: 8px; font: inherit; font-size: .9rem; font-weight: 650; transition: .18s ease;
      }
      .segment.selected { background: var(--ha-card-background, var(--card-background-color)); box-shadow: 0 3px 12px color-mix(in srgb, black 12%, transparent); }
      .segment-on.selected { color: var(--set-accent-on); border: 1px solid color-mix(in srgb, var(--set-accent-on) 35%, transparent); }
      .segment-off.selected { color: var(--set-accent-off); border: 1px solid color-mix(in srgb, var(--set-accent-off) 35%, transparent); }
      .segment:disabled { cursor: default; opacity: .65; }
      .duration-control { display: grid; grid-template-columns: minmax(88px, 1fr) minmax(150px, 1.45fr) minmax(88px, 1fr); gap: 10px; align-items: stretch; }
      .step-button {
        min-height: 62px; border: 1px solid var(--set-border); border-radius: 14px; background: var(--set-surface); color: var(--primary-text-color);
        cursor: pointer; display: flex; flex-direction: column; gap: 3px; align-items: center; justify-content: center; font: inherit; font-weight: 650;
      }
      .step-button ha-icon { color: var(--set-accent); }
      .step-button span { font-size: .72rem; color: var(--set-muted); }
      button:disabled { opacity: .45; cursor: default; }
      .time-inputs {
        min-height: 62px; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; border: 1px solid color-mix(in srgb, var(--set-accent) 45%, var(--set-border));
        border-radius: 15px; background: color-mix(in srgb, var(--set-accent) 7%, transparent); padding: 7px 10px;
      }
      .time-inputs label { display: grid; justify-items: center; gap: 1px; }
      .time-inputs input {
        width: 100%; min-width: 0; border: 0; outline: 0; background: transparent; color: var(--primary-text-color); text-align: center;
        font: inherit; font-size: 1.65rem; font-weight: 760; line-height: 1; appearance: textfield;
      }
      .time-inputs input::-webkit-inner-spin-button { appearance: none; }
      .time-inputs label span { color: var(--set-muted); font-size: .67rem; font-weight: 650; }
      .time-separator { font-size: 1.5rem; font-weight: 800; color: var(--set-accent); align-self: start; padding-top: 2px; }
      .time-inputs.locked { opacity: .75; }
      .quick-grid { display: flex; flex-wrap: wrap; gap: 8px; }
      .quick-button {
        border: 1px solid color-mix(in srgb, var(--set-quick-color) 34%, var(--set-border)); border-radius: 999px; padding: 8px 12px;
        background: color-mix(in srgb, var(--set-quick-color) 7%, transparent); color: var(--set-quick-color);
        font: inherit; font-size: .78rem; font-weight: 650; cursor: pointer; transition: .15s ease;
      }
      .quick-button.selected { color: var(--set-quick-selected-color); border-color: color-mix(in srgb, var(--set-quick-selected-color) 64%, var(--set-border)); background: color-mix(in srgb, var(--set-quick-selected-color) 15%, transparent); }
      .progress-section { padding: 13px; border: 1px solid var(--set-border); background: var(--set-surface); border-radius: 15px; gap: 10px; }
      .progress-heading { display: flex; justify-content: space-between; gap: 12px; align-items: baseline; }
      .progress-heading span, .time-mode span, .ring-center span { color: var(--set-muted); font-size: .8rem; }
      .progress-heading strong { color: var(--set-progress-color); font-variant-numeric: tabular-nums; font-size: 1.05rem; letter-spacing: .02em; }
      .progress-track { height: 9px; overflow: hidden; border-radius: 999px; background: color-mix(in srgb, var(--primary-text-color) 10%, transparent); }
      .progress-fill { height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--set-progress-color), color-mix(in srgb, var(--set-progress-color) 65%, var(--primary-color))); transition: width .35s linear; }
      .ring-mode { display: grid; place-items: center; padding: 4px 0; }
      .ring-wrap { position: relative; width: min(160px, 52vw); aspect-ratio: 1; }
      .ring-wrap svg { width: 100%; height: 100%; transform: rotate(-90deg); }
      .ring-wrap circle { fill: none; stroke-width: 9; }
      .ring-track { stroke: color-mix(in srgb, var(--primary-text-color) 10%, transparent); }
      .ring-value { stroke: var(--set-progress-color); stroke-linecap: round; transition: stroke-dasharray .35s linear; }
      .ring-center { position: absolute; inset: 0; display: grid; place-content: center; justify-items: center; gap: 3px; text-align: center; }
      .ring-center strong { max-width: 120px; color: var(--set-progress-color); font-size: 1.16rem; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
      .time-mode { min-height: 72px; display: grid; place-content: center; justify-items: center; gap: 4px; text-align: center; }
      .time-mode strong { color: var(--set-progress-color); font-size: 1.7rem; font-variant-numeric: tabular-nums; letter-spacing: .02em; }
      .status-message { display: grid; grid-template-columns: auto 1fr; gap: 9px; align-items: start; padding-top: 2px; }
      .status-indicator { width: 8px; height: 8px; margin-top: 5px; border-radius: 50%; background: var(--set-muted); }
      .status-message > div { display: grid; gap: 1px; min-width: 0; }
      .status-message strong { font-size: .76rem; }
      .status-message span:last-child { color: var(--set-muted); font-size: .75rem; overflow-wrap: anywhere; }
      .status-message.active .status-indicator, .status-message.ready .status-indicator { background: var(--set-accent); box-shadow: 0 0 0 4px color-mix(in srgb, var(--set-accent) 14%, transparent); }
      .status-message.success .status-indicator { background: var(--success-color, #2eaf68); }
      .status-message.warning .status-indicator { background: var(--warning-color, #e8843d); }
      .status-message.error .status-indicator { background: var(--error-color, #db4437); }
      footer { display: grid; grid-template-columns: 1.3fr 1fr; gap: 10px; }
      footer button {
        min-height: 48px; border-radius: 13px; border: 1px solid transparent; cursor: pointer; display: flex; align-items: center; justify-content: center;
        gap: 8px; font: inherit; font-size: .9rem; font-weight: 720; transition: transform .12s ease, opacity .12s ease;
      }
      footer button:not(:disabled):active, .step-button:not(:disabled):active, .segment:not(:disabled):active, .quick-button:not(:disabled):active { transform: scale(.98); }
      .primary-action.start-ready { color: white; background: linear-gradient(135deg, var(--set-start-color), color-mix(in srgb, var(--set-start-color) 68%, black)); box-shadow: 0 6px 18px color-mix(in srgb, var(--set-start-color) 25%, transparent); }
      .primary-action.timer-active { color: white; background: var(--set-timer-active-color); border-color: color-mix(in srgb, var(--set-timer-active-color) 75%, transparent); }
      .primary-action.start-disabled { color: var(--set-inactive-color); background: color-mix(in srgb, var(--set-inactive-color) 9%, transparent); border-color: color-mix(in srgb, var(--set-inactive-color) 24%, transparent); }
      .cancel-action.cancel-ready { color: white; border-color: var(--set-cancel-color); background: var(--set-cancel-color); }
      .cancel-action.inactive-state { color: var(--set-inactive-color); border-color: color-mix(in srgb, var(--set-inactive-color) 24%, transparent); background: color-mix(in srgb, var(--set-inactive-color) 8%, transparent); }
      footer button:disabled { box-shadow: none; filter: none; opacity: .62; }
      .primary-action.timer-active:disabled { opacity: .88; }
      .setup { min-height: 180px; padding: 26px; display: grid; gap: 10px; place-content: center; justify-items: center; text-align: center; color: var(--secondary-text-color); }
      .setup strong { color: var(--primary-text-color); font-size: 1rem; }
      .setup-icon { font-size: 2rem; }
      .setup code { padding: 5px 8px; border-radius: 7px; background: var(--set-surface); }
      .error-panel strong { color: var(--error-color); }
      .spinner { width: 28px; height: 28px; border: 3px solid var(--set-border); border-top-color: var(--primary-color); border-radius: 50%; animation: spin .8s linear infinite; }
      @keyframes spin { to { transform: rotate(360deg); } }


      /* Density controls spacing without changing available features. */
      .density-tight .content { gap: 10px; padding: 12px; }
      .density-tight header { gap: 9px; }
      .density-tight .entity-icon { width: 38px; height: 38px; border-radius: 11px; }
      .density-tight .entity-icon ha-icon { --mdc-icon-size: 23px; }
      .density-tight .title { font-size: 1rem; }
      .density-tight .subtitle { margin-top: 1px; font-size: .74rem; }
      .density-tight .action-badge { padding: 4px 8px; font-size: .66rem; gap: 5px; }
      .density-tight .badge-dot { width: 6px; height: 6px; box-shadow: none; }
      .density-tight section { gap: 5px; }
      .density-tight .segment { min-height: 34px; font-size: .8rem; }
      .density-tight .segmented { padding: 3px; gap: 4px; border-radius: 10px; }
      .density-tight .step-button, .density-tight .time-inputs { min-height: 46px; }
      .density-tight .step-button { border-radius: 10px; }
      .density-tight .step-button span { font-size: .64rem; }
      .density-tight .time-inputs { border-radius: 11px; padding: 4px 7px; }
      .density-tight .time-inputs input { font-size: 1.3rem; }
      .density-tight .time-separator { font-size: 1.15rem; }
      .density-tight .quick-grid { gap: 5px; }
      .density-tight .quick-button { padding: 5px 8px; font-size: .7rem; }
      .density-tight .progress-section { padding: 8px; gap: 6px; border-radius: 11px; }
      .density-tight .progress-track { height: 6px; }
      .density-tight .time-mode { min-height: 48px; }
      .density-tight .time-mode strong { font-size: 1.35rem; }
      .density-tight footer { gap: 7px; }
      .density-tight footer button { min-height: 40px; border-radius: 10px; font-size: .82rem; }

      /* Flat: solid colors, visible borders, no elevation or gradients. */
      .style-flat { box-shadow: none; border: 1px solid var(--set-border); border-radius: 10px; }
      .style-flat .accent { height: 3px; background: var(--set-accent); }
      .style-flat .entity-icon, .style-flat .target-state, .style-flat .segmented, .style-flat .step-button, .style-flat .time-inputs, .style-flat .quick-button, .style-flat .progress-section {
        box-shadow: none; background: transparent; border-radius: 8px;
      }
      .style-flat .segment.selected { box-shadow: none; color: white; }
      .style-flat .segment-on.selected { background: var(--set-accent-on); border-color: var(--set-accent-on); }
      .style-flat .segment-off.selected { background: var(--set-accent-off); border-color: var(--set-accent-off); }
      .style-flat .primary-action.start-ready { background: var(--set-start-color); box-shadow: none; }
      .style-flat .primary-action.timer-active { background: var(--set-timer-active-color); }
      .style-flat .progress-fill { background: var(--set-progress-color); }
      .style-flat .quick-button.selected { color: white; background: var(--set-quick-selected-color); border-color: var(--set-quick-selected-color); }

      /* Minimal: remove decorative containers and keep only essential visual hierarchy. */
      .style-minimal { border-radius: var(--ha-card-border-radius, 10px); box-shadow: none; }
      .style-minimal .accent { display: none; }
      .style-minimal .content { padding: 11px 13px; gap: 10px; }
      .style-minimal .entity-icon { width: 36px; height: 36px; border-radius: 8px; background: transparent; }
      .style-minimal .entity-icon ha-icon { --mdc-icon-size: 23px; }
      .style-minimal .title { font-size: 1rem; }
      .style-minimal .subtitle { font-size: .74rem; }
      .style-minimal .action-badge { padding: 4px 7px; font-size: .65rem; background: transparent; border: 1px solid currentColor; }
      .style-minimal .target-state { border: 0; border-bottom: 1px solid var(--set-border); border-radius: 0; background: transparent; padding: 6px 0 8px; }
      .style-minimal .section-label { font-size: .7rem; text-transform: uppercase; letter-spacing: .06em; }
      .style-minimal .segmented { padding: 0; gap: 12px; border: 0; border-radius: 0; background: transparent; }
      .style-minimal .segment { min-height: 36px; border-radius: 0; border-bottom: 2px solid transparent; }
      .style-minimal .segment.selected { background: transparent; box-shadow: none; }
      .style-minimal .segment-on.selected { border: 0; border-bottom: 2px solid var(--set-accent-on); color: var(--set-accent-on); }
      .style-minimal .segment-off.selected { border: 0; border-bottom: 2px solid var(--set-accent-off); color: var(--set-accent-off); }
      .style-minimal .duration-control { gap: 6px; }
      .style-minimal .step-button { min-height: 48px; border: 0; border-radius: 6px; background: transparent; }
      .style-minimal .time-inputs { min-height: 48px; border: 0; border-bottom: 2px solid var(--set-accent); border-radius: 0; background: transparent; padding: 4px 8px; }
      .style-minimal .time-inputs input { font-size: 1.45rem; }
      .style-minimal .quick-grid { gap: 10px; }
      .style-minimal .quick-button { padding: 5px 3px; border: 0; border-bottom: 2px solid color-mix(in srgb, var(--set-quick-color) 35%, transparent); border-radius: 0; background: transparent; }
      .style-minimal .quick-button.selected { background: transparent; border-bottom-color: var(--set-quick-selected-color); color: var(--set-quick-selected-color); }
      .style-minimal .progress-section { padding: 4px 0; border: 0; border-radius: 0; background: transparent; }
      .style-minimal .progress-track { height: 6px; }
      .style-minimal .progress-fill { background: var(--set-progress-color); }
      .style-minimal footer { gap: 7px; }
      .style-minimal footer button { min-height: 40px; border-radius: 7px; }
      .style-minimal .primary-action.start-ready { background: var(--set-start-color); box-shadow: none; }
      .style-minimal .status-message.active .status-indicator, .style-minimal .status-message.ready .status-indicator { box-shadow: none; }

      @container (max-width: 410px) {
        .content { padding: 15px; gap: 14px; }
        header { grid-template-columns: auto minmax(0,1fr); }
        .action-badge { grid-column: 1 / -1; justify-self: stretch; justify-content: center; }
        .target-state { grid-template-columns: 1fr auto; }
        .raw-state { display: none; }
        .duration-control { grid-template-columns: 1fr 1fr; }
        .time-inputs { grid-column: 1 / -1; grid-row: 1; }

        /* 0.3.0: inline action buttons must stay on one row on phones. */
        footer.buttons-inline { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
        footer.buttons-primary_only { grid-template-columns: 1fr; }

        /* Mini/Tile keep duration controls in a single compact row on phones. */
        .mini .duration-control, .tile .duration-control {
          grid-template-columns: 50px minmax(0, 1fr) 50px;
          gap: 6px;
        }
        .mini .time-inputs, .tile .time-inputs {
          grid-column: auto;
          grid-row: auto;
        }
      }

      .compact .target-state, .compact .section-label { display: none; }
      .compact .content { gap: 12px; }
      .compact .progress-section { padding: 11px; }
      .expanded .content { padding: 22px; gap: 18px; }

      /* Mini: mobile-first, about half the vertical footprint of the full card. */
      .mini .accent { height: 3px; }
      .mini .content { padding: 11px 12px 12px; gap: 8px; }
      .mini header { grid-template-columns: auto minmax(0,1fr) auto; gap: 8px; }
      .mini .entity-icon { width: 34px; height: 34px; border-radius: 10px; }
      .mini .entity-icon ha-icon { --mdc-icon-size: 21px; }
      .mini .title { font-size: .98rem; }
      .mini .subtitle { display: none; }
      .mini .action-badge { padding: 4px 7px; font-size: .64rem; }
      .mini .section-label { display: none; }
      .mini .segmented { padding: 2px; border-radius: 9px; }
      .mini .segment { min-height: 32px; font-size: .76rem; gap: 5px; }
      .mini .segment ha-icon { --mdc-icon-size: 18px; }
      .mini .duration-control {
        grid-template-columns: 50px minmax(120px,1fr) 50px;
        gap: 6px;
      }
      .mini .step-button { min-height: 44px; border-radius: 10px; }
      .mini .step-button ha-icon { --mdc-icon-size: 20px; }
      .mini .step-button span { font-size: .6rem; }
      .mini .time-inputs { min-height: 44px; border-radius: 10px; padding: 3px 6px; }
      .mini .time-inputs input { font-size: 1.23rem; }
      .mini .time-inputs label span { font-size: .59rem; }
      .mini .time-separator { font-size: 1.08rem; }
      .mini .quick-grid {
        flex-wrap: nowrap;
        gap: 4px;
        overflow-x: auto;
        scrollbar-width: none;
        padding-bottom: 1px;
      }
      .mini .quick-grid::-webkit-scrollbar { display: none; }
      .mini .quick-button {
        flex: 0 0 auto;
        padding: 4px 7px;
        font-size: .68rem;
      }
      .mini .progress-section { padding: 7px 8px; gap: 5px; border-radius: 10px; }
      .mini .progress-heading span { font-size: .7rem; }
      .mini .progress-heading strong { font-size: .9rem; }
      .mini .progress-track { height: 5px; }
      .mini .ring-wrap { width: min(94px, 32vw); }
      .mini .ring-wrap circle { stroke-width: 8; }
      .mini .ring-center strong { font-size: .92rem; }
      .mini .ring-center span { font-size: .66rem; }
      .mini .time-mode { min-height: 42px; }
      .mini .time-mode strong { font-size: 1.2rem; }
      .mini .status-message { align-items: center; gap: 7px; }
      .mini .status-indicator { margin-top: 0; }
      .mini .status-message strong { font-size: .72rem; }
      .mini .status-message span:last-child { display: none; }
      .mini .status-message.error span:last-child,
      .mini .status-message.warning span:last-child { display: block; font-size: .68rem; }
      .mini footer button { min-height: 38px; border-radius: 9px; font-size: .8rem; }

      /* Tile: only the essential timer control, ideal below a climate card or in a grid. */
      .tile .accent { height: 2px; }
      .tile .content { padding: 9px 10px 10px; gap: 7px; }
      .tile header { grid-template-columns: auto minmax(0,1fr) auto; gap: 7px; }
      .tile .entity-icon { width: 30px; height: 30px; border-radius: 9px; }
      .tile .entity-icon ha-icon { --mdc-icon-size: 19px; }
      .tile .title { font-size: .9rem; }
      .tile .subtitle { display: none; }
      .tile .action-badge { padding: 3px 6px; font-size: .6rem; gap: 4px; }
      .tile .badge-dot { width: 5px; height: 5px; box-shadow: none; }
      .tile .section-label { display: none; }
      .tile .segmented { padding: 2px; gap: 3px; border-radius: 8px; }
      .tile .segment { min-height: 29px; font-size: .7rem; gap: 4px; }
      .tile .segment ha-icon { --mdc-icon-size: 16px; }
      .tile .duration-control {
        grid-template-columns: 44px minmax(105px,1fr) 44px;
        gap: 5px;
      }
      .tile .step-button { min-height: 40px; border-radius: 9px; }
      .tile .step-button ha-icon { --mdc-icon-size: 19px; }
      .tile .step-button span { display: none; }
      .tile .time-inputs { min-height: 40px; border-radius: 9px; padding: 2px 5px; }
      .tile .time-inputs input { font-size: 1.08rem; }
      .tile .time-inputs label span { font-size: .55rem; }
      .tile .time-separator { font-size: .98rem; padding-top: 1px; }
      .tile .quick-grid {
        flex-wrap: nowrap;
        gap: 4px;
        overflow-x: auto;
        scrollbar-width: none;
      }
      .tile .quick-grid::-webkit-scrollbar { display: none; }
      .tile .quick-button { flex: 0 0 auto; padding: 3px 6px; font-size: .64rem; }
      .tile .progress-section { padding: 6px 7px; gap: 4px; border-radius: 9px; }
      .tile .progress-heading span { font-size: .66rem; }
      .tile .progress-heading strong { font-size: .84rem; }
      .tile .progress-track { height: 4px; }
      .tile .ring-wrap { width: min(78px, 28vw); }
      .tile .ring-wrap circle { stroke-width: 8; }
      .tile .ring-center strong { font-size: .82rem; }
      .tile .ring-center span { font-size: .6rem; }
      .tile .time-mode { min-height: 36px; }
      .tile .time-mode strong { font-size: 1.05rem; }
      .tile footer { gap: 5px; }
      .tile footer button { min-height: 36px; border-radius: 8px; font-size: .76rem; }

      /* Button presentation. */
      footer.buttons-inline { grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr); }
      footer.buttons-primary_only { grid-template-columns: 1fr; }

      @media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
    </style>`;
  }
}

if (!customElements.get("smart-entity-timer-card")) customElements.define("smart-entity-timer-card", SmartEntityTimerCard);

window.customCards = window.customCards || [];
if (!window.customCards.some((card) => card.type === "smart-entity-timer-card")) {
  window.customCards.push({
    type: "smart-entity-timer-card",
    name: "Smart Entity Timer Card",
    description: "A configurable visual timer card for the Smart Entity Timer integration.",
    preview: false,
    documentationURL: "https://github.com/abel-smart-timer/smart-entity-timer",
    getEntitySuggestion: (hass, entityId) => {
      const state = hass?.states?.[entityId];
      const compatible = entityDomain(entityId) === "sensor" && Number(state?.attributes?.card_api_version) >= MIN_CARD_API_VERSION && Boolean(state?.attributes?.backend_version);
      if (!compatible) return null;
      return {
        config: {
          type: "custom:smart-entity-timer-card",
          entity: entityId,
          increment_minutes: 30,
          layout: "auto",
          visual_style: "modern",
          action_mode: "selectable",
          button_mode: "auto",
          progress_style: "bar",
          time_format: "auto",
          show_header: true,
          show_target_state: true,
          show_action_selector: true,
          show_duration_controls: true,
          show_quick_times: true,
          show_progress: true,
          show_status: true,
          show_last_result: true,
        },
      };
    },
  });
}

console.info(
  `%c SMART ENTITY TIMER CARD %c ${CARD_VERSION} `,
  "color: white; background: #5c4bdb; font-weight: 700; padding: 3px 5px; border-radius: 4px 0 0 4px;",
  "color: #5c4bdb; background: #eeeafd; font-weight: 700; padding: 3px 5px; border-radius: 0 4px 4px 0;",
);

export {
  CARD_VERSION,
  SmartEntityTimerCard,
  formatClock,
  formatTimeValue,
  normalizeColor,
  parseQuickTimes,
  targetReached,
};
