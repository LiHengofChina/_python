003_lanzhou — 兰州精简识别训练包
================================
仅保留 9 类：
  DEFAULT / NAME / PHONE / LANDLINE / CREDIT_CODE
  ID_CARD / OFFICER_CARD / PASSPORT / ENTERPRISE_NAME

相对 002 的裁剪：
1) fit_data：仅 9 个 CSV；其它原类型已改标 DEFAULT 后并入 DEFAULT.csv，
   原文件在 fit_data/_legacy/unused_labels/
2) test_sample：仅 9 类；其它在 _legacy/unused_test_sample/
3) rklink_002.py：加载/测试/后处理仅处理 KEEP_LABELS
4) 特征维数仍为 136（与 Java ColumnFeatureExtractor 对齐）
5) 训练结束默认同步到：
   D:\___workspace\workspace_2025_18_w_java_\datasharingplatform\mask-sdk\src\main\resources\recognize_model
   可用环境变量 MASK_SDK_RECOGNIZE_MODEL_DIR 覆盖；设为空字符串则跳过同步

后续：重新运行 rklink_003.py 训练（会同步 PMML 到 mask-sdk）。

当前 fit_data：
- 每列固定 20 行（对齐现场）
- 正类约 100 列 × 20 = 2000 行/类
- DEFAULT 约 1500 列 × 20 = 30000 行
- 正类已按列注入噪音 Uniform(10%,50%)（脚本 inject_noise_fit_data.py）
  · 其余行均为该类型正确样本（purify 通过）
  · 整文件 text 不重复（dup=0）
  · 干净备份在 fit_data/_legacy/before_noise/；重复跑会先恢复再重建
- DEFAULT 未掺脏（本身已是负样本）
