[上传]
python upload_bp_s3.py 								---- 上传 TestServer 中 promotion & banner		刷新 promotion.json
python upload_s3_resource_dynamic.py 				---- 上传 TestServer 中 res & dynamic			刷新 prerelease/*
python upload_s3.py 								---- 上传 TestServer							刷新 promotion.json, prerelease/*

python upload_s3.py 1.21.252						---- 上传 TestServer/1.21.252					不刷新
python upload_s3.py banner							---- 上传 TestServer/banner						不刷新
python upload_s3.py promotion						---- 上传 TestServer/promotion					不刷新
python upload_s3.py dynamic							---- 上传 TestServer/dynamic 					不刷新
python upload_s3.py dynamic/31						---- 上传 TestServer/dynamic/31 				不刷新

python upload_s3_promotiononly.py					---- 上传 TestServer/promotion					不刷新
python upload_s3_banneronly.py						---- 上传 TestServer/banner						不刷新

[预发布]
python prerelease_bp_s3.py 							---- 预发布 TestServer 4个版本号到 prerelease	刷新 prerelease/*
python prerelease_bp_s3.py 1234						---- 预发布 TestServer 4个版本号到 prerelease
														 指定 promotion & banner 版本号为 1234		刷新 prerelease/*

[发布]
python publish_s3.py 								---- 发布 prerelease 目录中 res, banner, promotion 3个版本号
																									刷新 batch.json, 根目录*
python publish_s3_resource_dynamic.py 				---- 发布 prerelease 目录中 res 版本号 			刷新 batch.json, 根目录*

python publish_increase_bpversion_s3.py 			---- 发布 促销版本号加1							刷新 promotion_version.bytes, banner_version.bytes
python publish_increase_bpversion_s3.py 1234		---- 发布 促销版本号改为 1234					刷新 promotion_version.bytes, banner_version.bytes

[刷新]
python invalid.py batch.json              			---- 刷新 批处理 TestServer/batch.json
python invalid.py promotion_version.bytes  			---- 刷新 文件 promotion_version.bytes
python invalid.py dynamic/5/*			  			---- 刷新 目录 dynamic/5 （不包含子目录）
python invalid.py promotion/dailypromotion*			---- 刷新 目录 promotion/dailypromotion （包含子目录）

python publish_invalid_all_s3.py 					---- 刷新 根目录的 4 个版本号文件 (res, banner, promotion, app)

[下载]
python download.py 20200220_ios/res_version.bytes	---- 下载 文件 20200220_ios/res_version.bytes
python download.py 20200220/1.21.246/				---- 下载 目录 20200220/1.21.246/	（要以 / 结尾）

[删除]
python delete_s3.py 								---- 删除 S3 目录、文件
