# 04 - User Identity Model
## Unified  Table Schema
- uid=1000(python) gid=1000(python) groups=1000(python),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),100(users),116(lpadmin),981(docker) (UUID, PK)
-  (VARCHAR(255), Unique, Indexed)
-  (VARCHAR(100))
-  (VARCHAR(255))
-  (UserRole: admin, manager, agent, customer)
-  (UserStatus: active, suspended)
-  (VARCHAR(50), Nullable, Indexed -> links to ShopKart )
- , , , , , ,
