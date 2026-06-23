recognize_model — mask-sdk 列类型识别模型包（RandomForest + PMML）
============================================================
本目录由 E 盘 rklink_002.py 训练输出，供 Java mask-sdk JPMML 本地推理。
Python 侧主输出在 002/output/recognize_model/；训练结束会整包覆盖同步到本目录。
主要文件：
  recognize_rf_model.pmml      — Java 推理（必需）
  recognize_rf_model.joblib    — 备份
  dicts/all_dicts.json         — 特征用字典
  dicts/mobile_prefixes.json  — 手机号段（规则后处理，由 dict/ 同步）
  dicts/area_codes.json       — 固话区号（规则后处理，由 dict/ 同步）
  dicts/id_card_region_prefixes.json — 身份证区划（由 zip_code.txt 派生）
  dicts/officer_card_first_chars.json — 军官证首字（由 dict/ 同步）
  feature_names.json           — f0..f135（136 维）
  confidence_thresholds.json   — 非 8 类门控类的 JSON 阈值

识别流程（与 Java mask-sdk 一致）：
  1) PMML 初选
  2) 8 类门控（NAME/PHONE/LANDLINE/ID_CARD/CREDIT_CODE/OFFICER_CARD/PASSPORT/ENTERPRISE_NAME）
     Java: masks.recognize-*-confidence-threshold / *-default-min-margin
     Python 测试: 环境变量 MASK_SDK_RECOGNIZE_*（见 rklink_002.py 顶部配置区）
  3) apply_recognize_overrides 拦截/抬升（与 RecognizeOverrideSupport 对齐）
