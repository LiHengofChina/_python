"""Probe Oracle instances — pick best for day_03 testing."""
from pathlib import Path
import oracledb

BASE = Path(__file__).resolve().parent
IC = BASE / "instantclient" / "instantclient_19_26"
oracledb.init_oracle_client(lib_dir=str(IC))

CANDIDATES = [
    {
        "name": "35.13 bbed (test03)",
        "host": "192.168.35.13", "port": 1521, "service": "bbed",
        "user": "test03", "password": "test03", "mode": None,
    },
    {
        "name": "35.25 TEST2 (lg_user)",
        "host": "192.168.35.25", "port": 1521, "service": "TEST2",
        "user": "lg_user", "password": "lg_user", "mode": None,
    },
    {
        "name": "100.50 prod (sys SYSDBA)",
        "host": "192.168.100.50", "port": 1521, "service": "prod",
        "user": "sys", "password": "Oracle123", "mode": oracledb.SYSDBA,
    },
]

for c in CANDIDATES:
    print(f"\n=== {c['name']} ===")
    try:
        kw = dict(user=c["user"], password=c["password"],
                  host=c["host"], port=c["port"], service_name=c["service"])
        if c["mode"]:
            kw["mode"] = c["mode"]
        with oracledb.connect(**kw) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT banner FROM v$version WHERE ROWNUM = 1")
                ver = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM user_tables")
                tbl = cur.fetchone()[0]
                print(f"OK  version={ver[:60]}...")
                print(f"    user_tables={tbl}")
    except Exception as e:
        print(f"FAIL {e}")
