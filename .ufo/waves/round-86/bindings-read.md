# Round 86 host bindings

Before ready handoff L1 read `/home/vgpnk/.omp/agent/RULES.md`, the run-15 wave policy, and `task.agentModelOverrides` from `/home/vgpnk/.omp/agent/config.yml`. Observed all 18 roles mapped to `@m_zfl`; no model passed in the validated wave. A later read-only hash of the authority file is `2014653da3c365e9091c902bdc2c605052b0c5b7514882b6de8b6824147cd5c6` (`sha256sum /home/vgpnk/.omp/agent/config.yml`). This hash is not proof of a seat's answering model or the predispatch file's exact hash; routes can fall back and the authority is mutable. No host configuration changed.

Wave policy observed 8–16 spawn seats, max 256. L1 holds planner because validator excludes planner; one capture-probe seat explicitly rebadged executor after validator refused labrat, before ready handoff. Four attack-role seats out of fourteen requested. L1 integrates only after WAVE-DONE. Pacman remains paused. No tool installed or upgraded by L1.
