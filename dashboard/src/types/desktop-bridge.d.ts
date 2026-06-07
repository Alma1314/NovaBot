export {};

declare global {
  interface BulinBotDesktopAppUpdateCheckResult {
    ok: boolean;
    reason?: string | null;
    currentVersion?: string;
    latestVersion?: string | null;
    hasUpdate: boolean;
  }

  interface BulinBotDesktopAppUpdateResult {
    ok: boolean;
    reason?: string | null;
  }

  interface BulinBotAppUpdaterBridge {
    checkForAppUpdate: () => Promise<BulinBotDesktopAppUpdateCheckResult>;
    installAppUpdate: () => Promise<BulinBotDesktopAppUpdateResult>;
  }

  interface Window {
    bulinbotAppUpdater?: BulinBotAppUpdaterBridge;
    bulinbotDesktop?: {
      isDesktop: boolean;
      isDesktopRuntime: () => Promise<boolean>;
      getBackendState: () => Promise<{
        running: boolean;
        spawning: boolean;
        restarting: boolean;
        canManage: boolean;
      }>;
      restartBackend: (authToken?: string | null) => Promise<{
        ok: boolean;
        reason: string | null;
      }>;
      stopBackend: () => Promise<{
        ok: boolean;
        reason: string | null;
      }>;
      onTrayRestartBackend?: (callback: () => void) => () => void;
    };
  }
}
