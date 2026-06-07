/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BULINBOT_RELEASE_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
