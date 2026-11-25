# Google Maps Reviews API（谷歌地图点评 API）

[English](#english) · [中文](#中文)

## English

This repo reads public Google Maps Reviews data with Python or curl. You can search businesses and places by keyword, read a place's details (address, phone, opening hours, rating) and its reviews, and list every review one reviewer has written. You need one EveryInfra API key. You do not need a Google account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 4 capabilities cost $1.39 per 1,000 calls (about $0.0014 per call). Failed calls and empty results are not charged. The EveryInfra Google Maps Reviews API has 5 capabilities, all listed on the platform page: <https://everyinfra.com/en/google-maps-reviews-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### Quick start

```bash
git clone https://github.com/everyinfra/google-maps-reviews-api.git
cd google-maps-reviews-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "coffee shop in Singapore" --out places.csv
python main.py place "<place url>" --out place.json
python main.py reviews "<place url>" --out reviews.csv
python main.py reviewer <reviewer_id> --out reviewer.csv
```

- The `search` keyword can include a city, for example coffee shop in Singapore. It searches places, not review text.
- For `place` and `reviews`, pass the `url` from a `search` result (the one with query_place_id). A /place/ link with only a name and coordinates may not find the same business.
- For `reviewer`, pass the `reviewer_id` from a `reviews` result, or the reviewer's profile link https://www.google.com/maps/contrib/<numeric id>. It returns up to 200 reviews.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- `--pages N` follows `next_page_token` for N pages. Each page counts as one call.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"google_maps_reviews","action":"search","params":{"keyword":"coffee shop in Singapore"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `profile`, `reviews`, and `contributor_reviews` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $1.39 |
| `profile` | $1.39 |
| `reviews` | $1.39 |
| `contributor_reviews` | $1.39 |

- Billing is per call, about $0.0014 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- Each page fetched with `--pages` counts as one call.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>
- Prices for the 1 other Google Maps Reviews capability are on the platform page: <https://everyinfra.com/en/google-maps-reviews-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### Fields

These are the fields that the 4 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `place_id` | Google place ID, a unique identifier shared across Google services. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `url` | Link to the record on the platform. |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `categories` | Place categories (restaurant, hotel and so on). |
| `description` | Summary or description, usually shorter than text. |
| `address` | Full address, passed through as is. |
| `city` | City name in the platform's language, not normalized. |
| `postal_code` | Postal code. |
| `country_code` | Country code. |
| `lat` | Latitude. |
| `lng` | Longitude. |
| `phone` | Contact phone number, passed through without format normalization. |
| `website` | External website entered by the account or business. |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `review_count` | Number of reviews, for product and business capabilities. null means not disclosed, not 0. |
| `image_url` | Image link. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/google-maps-reviews-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

#### `profile` (profile or object details)

| Field | Meaning |
|---|---|
| `place_id` | Google place ID, a unique identifier shared across Google services. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `url` | Link to the record on the platform. |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `categories` | Place categories (restaurant, hotel and so on). |
| `description` | Summary or description, usually shorter than text. |
| `address` | Full address, passed through as is. |
| `neighborhood` | Neighborhood where the place is located. |
| `city` | City name in the platform's language, not normalized. |
| `postal_code` | Postal code. |
| `country_code` | Country code. |
| `plus_code` | Google Plus Code (open location code); used to locate places without street addresses. |
| `lat` | Latitude. |
| `lng` | Longitude. |
| `phone` | Contact phone number, passed through without format normalization. |
| `website` | External website entered by the account or business. |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `review_count` | Number of reviews, for product and business capabilities. null means not disclosed, not 0. |
| `image_count` | Number of images of the place on Google Maps (profile). |
| `price` | Price as a number without a currency symbol; see currency. |
| `permanently_closed` | Whether the place is permanently closed. |
| `temporarily_closed` | Whether the place is temporarily closed. |
| `opening_hours` | Opening hours schedule. |
| `image_url` | Image link. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/google-maps-reviews-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

#### `reviews` (reviews)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `reviewer_name` | Reviewer name. |
| `reviewer_id` | The reviewer's Google Maps ID (the number after /maps/contrib/ in the reviewer's profile link). |
| `reviewer_review_count` | Total number of reviews the reviewer has written. |
| `is_local_guide` | Whether the reviewer is a Google Local Guide (a certification for active reviewers). |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `url` | Link to the record on the platform. |
| `detailed_rating` | Ratings by aspect (food, service, atmosphere and so on). |
| `place_id` | Google place ID, a unique identifier shared across Google services. |
| `place_name` | Place name. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `image_urls` | Array of image links in the platform's display order; absent when there are no images. |

All parameters and fields: <https://everyinfra.com/en/google-maps-reviews-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

#### `contributor_reviews` (contributor reviews)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `posted_ago` | Relative publish time (such as 13 hours ago), measured from the time of capture. |
| `url` | Link to the record on the platform. |
| `image_urls` | Array of image links in the platform's display order; absent when there are no images. |
| `place_name` | Place name. |
| `place_address` | Address of the reviewed place. |
| `place_type` | Type of the reviewed place (such as Restaurant, Corporate office). |
| `place_data_id` | Google Maps data_id of the reviewed place (in the form 0x…:0x…); can be used to identify the same place. |
| `lat` | Latitude. |
| `lng` | Longitude. |
| `reviewer_name` | Reviewer name. |
| `reviewer_id` | The reviewer's Google Maps ID (the number after /maps/contrib/ in the reviewer's profile link). |
| `reviewer_review_count` | Total number of reviews the reviewer has written. |
| `is_local_guide` | Whether the reviewer is a Google Local Guide (a certification for active reviewers). |
| `local_guide_level` | The reviewer's Local Guide level (1-10). |
| `local_guide_points` | The reviewer's Local Guide points. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |
| `owner_response` | The business's public reply to this review: text, author_name and posted_at; absent when there is no reply. |
| `owner_response_ago` | Relative time of the owner's response (such as 2 weeks ago). |

All parameters and fields: <https://everyinfra.com/en/google-maps-reviews-api/contributor_reviews?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### FAQ

**Do I need a Google account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $1.39 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

**Can I connect the Google Maps Reviews API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>.

**What legal points apply when I use Google Maps Reviews data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Google Maps Reviews data can I get?**

The EveryInfra Google Maps Reviews API has 5 capabilities:

- keyword search
- profile or object details
- reviews
- contributor reviews
- business listings

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/google-maps-reviews-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### Tested

Before release, we ran the 4 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "coffee shop in Singapore" --out places.csv` | 2026-11-25 12:45 | 15 | $0.001389 |
| `python main.py place "<place url>" --out place.json` | 2026-11-25 12:45 | 1 | $0.001389 |
| `python main.py reviews "<place url>" --out reviews.csv` | 2026-11-25 12:45 | 20 | $0.001389 |
| `python main.py reviewer <reviewer_id> --out reviewer.csv` | 2026-11-25 12:46 | 20 | $0.001389 |

## 中文

本仓库用 Python 或 curl 读谷歌地图点评公开数据：按关键词搜商户和地点，读商户资料（地址、电话、营业时间、评分）和用户评论，再看某位点评人写过的全部评论。只需一把 EveryInfra API Key，不用 Google 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 4 个能力每千次 $1.39（每次约 $0.0014），失败和空结果不收费。谷歌地图点评共 5 个能力：<https://everyinfra.com/google-maps-reviews-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/google-maps-reviews-api.git
cd google-maps-reviews-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "coffee shop in Singapore" --out places.csv
python main.py place "<地点链接>" --out place.json
python main.py reviews "<地点链接>" --out reviews.csv
python main.py reviewer <reviewer_id> --out reviewer.csv
```

- `search` 的关键词可以带城市，比如 coffee shop in Singapore；它查地点，不是在评论里全文搜。
- `place` 和 `reviews` 传 `search` 结果里的 `url`（带 query_place_id 的那种），只有店名和坐标的 /place/ 链接可能定位不到同一家店。
- `reviewer` 传 `reviews` 结果里的 `reviewer_id`，也可以传点评人主页链接 https://www.google.com/maps/contrib/<数字 ID>，最多返回 200 条。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- `--pages N` 按 `next_page_token` 翻页，每翻一页算一次调用。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"google_maps_reviews","action":"search","params":{"keyword":"coffee shop in Singapore"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`profile`、`reviews`、`contributor_reviews` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $1.39 |
| 主页或对象详情 | `profile` | $1.39 |
| 评价 | `reviews` | $1.39 |
| 点评人的全部评价 | `contributor_reviews` | $1.39 |

- 按调用次数计费，每次约 $0.0014；失败、空结果、参数错误和鉴权失败都不收费。
- `--pages` 翻的每一页算一次调用。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>
- 谷歌地图点评其他 1 个能力的单价见平台页 <https://everyinfra.com/google-maps-reviews-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### 返回字段

下面是这 4 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `place_id` | Google 地点 ID，跨 Google 服务通用的唯一标识。 |
| `name` | 名称。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `category` | 分类名称，取值为原平台的分类体系，未做跨平台归一。 |
| `categories` | 地点分类（餐厅/酒店等）。 |
| `description` | 简介或描述，通常比 text 短。 |
| `address` | 详细地址，原文透传。 |
| `city` | 城市名，用原平台的语言书写，未做中英归一。 |
| `postal_code` | 邮编。 |
| `country_code` | 国家代码。 |
| `lat` | 纬度。 |
| `lng` | 经度。 |
| `phone` | 联系电话，原文透传，未做号码格式归一。 |
| `website` | 账号或商家填写的外链网址。 |
| `rating` | 评分。 |
| `review_count` | 评价条数，用于商品/商家类能力。 |
| `image_url` | 图片链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/google-maps-reviews-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

#### `profile`（主页或对象详情）

| 字段 | 含义 |
|---|---|
| `place_id` | Google 地点 ID，跨 Google 服务通用的唯一标识。 |
| `name` | 名称。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `category` | 分类名称，取值为原平台的分类体系，未做跨平台归一。 |
| `categories` | 地点分类（餐厅/酒店等）。 |
| `description` | 简介或描述，通常比 text 短。 |
| `address` | 详细地址，原文透传。 |
| `neighborhood` | 所在街区。 |
| `city` | 城市名，用原平台的语言书写，未做中英归一。 |
| `postal_code` | 邮编。 |
| `country_code` | 国家代码。 |
| `plus_code` | Google Plus Code（开放位置编码），无门牌地址地区用它定位。 |
| `lat` | 纬度。 |
| `lng` | 经度。 |
| `phone` | 联系电话，原文透传，未做号码格式归一。 |
| `website` | 账号或商家填写的外链网址。 |
| `rating` | 评分。 |
| `review_count` | 评价条数，用于商品/商家类能力。 |
| `image_count` | 该地点在 Google Maps 上的图片数量（profile）。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `permanently_closed` | 是否已永久停业。 |
| `temporarily_closed` | 是否临时歇业。 |
| `opening_hours` | 营业时间表。 |
| `image_url` | 图片链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/google-maps-reviews-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

#### `reviews`（评价）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `rating` | 评分。 |
| `reviewer_name` | 点评人名称。 |
| `reviewer_id` | 点评人的 Google 地图 ID（点评人主页链接 /maps/contrib/ 后面那串数字）。 |
| `reviewer_review_count` | 点评人的历史点评总数。 |
| `is_local_guide` | 是否为 Google 本地向导（活跃点评者认证）。 |
| `like_count` | 点赞数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `detailed_rating` | 分维度评分（食物/服务/氛围等）。 |
| `place_id` | Google 地点 ID，跨 Google 服务通用的唯一标识。 |
| `place_name` | 地点名称。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `image_urls` | 点评附图。 |

完整参数和字段：<https://everyinfra.com/google-maps-reviews-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

#### `contributor_reviews`（点评人的全部评价）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `rating` | 评分。 |
| `like_count` | 点赞数。 |
| `posted_ago` | 发布时间的相对说法（如 13 hours ago），以抓取时刻为准；平台没给绝对时间时只有它。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `image_urls` | 点评附图。 |
| `place_name` | 地点名称。 |
| `place_address` | 被评地点的地址。 |
| `place_type` | 被评地点的类型（如 Restaurant、Corporate office）。 |
| `place_data_id` | 被评地点的 Google 地图 data_id（0x…:0x… 形式），可用来定位同一地点。 |
| `lat` | 纬度。 |
| `lng` | 经度。 |
| `reviewer_name` | 点评人名称。 |
| `reviewer_id` | 点评人的 Google 地图 ID（点评人主页链接 /maps/contrib/ 后面那串数字）。 |
| `reviewer_review_count` | 点评人的历史点评总数。 |
| `is_local_guide` | 是否为 Google 本地向导（活跃点评者认证）。 |
| `local_guide_level` | 点评人的本地向导等级（1–10）。 |
| `local_guide_points` | 点评人的本地向导积分。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |
| `owner_response` | 商家对点评的回复。 |
| `owner_response_ago` | 商家回复时间的相对说法（如 2 weeks ago）。 |

完整参数和字段：<https://everyinfra.com/google-maps-reviews-api/contributor_reviews?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### 常见问题

**调用时要不要提供 Google 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $1.39 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

**能把谷歌地图点评接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>。

**用谷歌地图点评数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到谷歌地图点评的哪些数据？**

谷歌地图点评有 5 个能力：关键词搜索、主页或对象详情、评价、点评人的全部评价、商家库检索。每个能力的参数和返回字段见平台页 <https://everyinfra.com/google-maps-reviews-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-reviews-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 4 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "coffee shop in Singapore" --out places.csv` | 2026-11-25 12:45 | 15 | $0.001389 |
| `python main.py place "<地点链接>" --out place.json` | 2026-11-25 12:45 | 1 | $0.001389 |
| `python main.py reviews "<地点链接>" --out reviews.csv` | 2026-11-25 12:45 | 20 | $0.001389 |
| `python main.py reviewer <reviewer_id> --out reviewer.csv` | 2026-11-25 12:46 | 20 | $0.001389 |

`profile` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "category": "Restaurant",
  "description": "Handcrafted salads & sandwiches, plus wine & spirits, in a c…",
  "rating": 4.7,
  "review_count": 8065,
  "image_count": 7796,
  "price": "SGD 20–40",
  "rating_scale": 5
}
```

## License

MIT
