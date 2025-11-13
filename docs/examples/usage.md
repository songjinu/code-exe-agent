# 💡 실전 사용 예시

이 문서는 생성된 디렉토리 구조를 실제로 어떻게 활용하는지 보여줍니다.

## 예시 1: Claude와 함께 사용

### 사용자 요청
```
"Salesforce에서 신규 계정을 만들고, 
그 계정에 연결된 영업 기회를 생성해줘"
```

### Claude의 작업 과정

#### Step 1: 디렉토리 탐색
```bash
> list servers/salesforce/
→ accounts/, opportunities/, contacts/, cases/, reports/, analytics/
```

#### Step 2: 필요한 도구 확인
```bash
> list servers/salesforce/accounts/
→ create.ts, update.ts, delete.ts, query.ts

> list servers/salesforce/opportunities/
→ create.ts, update.ts, close.ts
```

#### Step 3: 도구 정의 읽기
```bash
> view servers/salesforce/accounts/create.ts
> view servers/salesforce/opportunities/create.ts
```

#### Step 4: 코드 생성 및 실행
```typescript
import { create as createAccount } from './servers/salesforce/accounts/create';
import { create as createOpportunity } from './servers/salesforce/opportunities/create';

// 1. 계정 생성
const account = await createAccount({
  name: 'Tech Innovations Inc',
  industry: 'Technology',
  website: 'https://techinnovations.example.com'
});

console.log('Account created:', account.id);

// 2. 영업 기회 생성
const opportunity = await createOpportunity({
  accountId: account.id,
  name: 'Q4 2025 Deal',
  stage: 'Prospecting',
  amount: 100000,
  closeDate: '2025-12-31'
});

console.log('Opportunity created:', opportunity.id);
console.log('Setup complete!');
```

**토큰 사용량:**
- 기존 방식 (모든 도구 로드): ~5,000 토큰
- 새 방식 (필요한 것만): ~300 토큰
- **절감: 94%** ✅

---

## 예시 2: GPT-4와 함께 사용 (Context에 포함)

### 프롬프트 구성

```python
# 관련 도구들을 프롬프트에 포함
relevant_tools = """
사용 가능한 도구:

**servers/salesforce/accounts/**
- create.ts: Create a new Salesforce account
  ```typescript
  interface CreateInput {
    name: string;
    industry?: string;
    website?: string;
  }
  export async function create(input: CreateInput): Promise<CreateResponse>
  ```

**servers/salesforce/opportunities/**
- create.ts: Create a new opportunity
  ```typescript
  interface CreateInput {
    accountId: string;
    name: string;
    stage: string;
    amount: number;
  }
  export async function create(input: CreateInput): Promise<CreateResponse>
  ```
"""

prompt = f"""
{relevant_tools}

사용자 요청: {user_query}

위 도구를 사용하여 TypeScript 코드를 작성하세요.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

---

## 예시 3: 복잡한 워크플로우

### 사용자 요청
```
"Google Drive에서 Q3 매출 스프레드시트를 읽어서,
매출이 $50k 이상인 계정들만 Salesforce에 업데이트해줘"
```

### 생성된 코드

```typescript
import { read as readSpreadsheet } from './servers/google-drive/spreadsheets/read';
import { update as updateAccount } from './servers/salesforce/accounts/update';

// 1. Google Drive에서 스프레드시트 읽기
const spreadsheet = await readSpreadsheet({
  spreadsheetId: 'abc123',
  range: 'Sheet1!A:D'
});

console.log('Spreadsheet loaded:', spreadsheet.values.length, 'rows');

// 2. 데이터 필터링 (실행 환경 내에서)
const highValueAccounts = spreadsheet.values
  .filter(row => {
    const revenue = parseFloat(row[3]); // D열: 매출
    return revenue >= 50000;
  })
  .map(row => ({
    accountId: row[0],   // A열: Account ID
    name: row[1],         // B열: Name
    revenue: row[3]       // D열: Revenue
  }));

console.log('Filtered accounts:', highValueAccounts.length);

// 3. Salesforce 업데이트 (병렬 처리)
const updatePromises = highValueAccounts.map(account =>
  updateAccount({
    id: account.accountId,
    data: {
      AnnualRevenue: account.revenue,
      LastUpdated: new Date().toISOString()
    }
  })
);

await Promise.all(updatePromises);

console.log('All accounts updated!');
```

**핵심 장점:**
- ✅ 스프레드시트 전체 데이터가 모델 context를 통과하지 않음
- ✅ 필터링 로직이 실행 환경에서 처리됨
- ✅ 최종 결과만 모델에 전달

---

## 예시 4: 에러 처리 및 재시도

```typescript
import { create as createAccount } from './servers/salesforce/accounts/create';
import { read as readDocument } from './servers/google-drive/documents/read';

async function processAccountCreation(documentId: string) {
  try {
    // 1. Google Drive에서 계정 정보 읽기
    const doc = await readDocument({ documentId });
    const accountData = parseAccountData(doc.content);
    
    // 2. Salesforce에 계정 생성
    const account = await createAccount(accountData);
    
    console.log('✅ Success:', account.id);
    return account;
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    
    // 재시도 로직
    if (error.code === 'RATE_LIMIT') {
      console.log('Rate limited, retrying in 5s...');
      await new Promise(resolve => setTimeout(resolve, 5000));
      return processAccountCreation(documentId);
    }
    
    throw error;
  }
}

function parseAccountData(content: string) {
  // 문서 내용 파싱 (실행 환경에서 처리)
  const lines = content.split('\n');
  return {
    name: lines[0],
    industry: lines[1],
    website: lines[2]
  };
}

// 실행
await processAccountCreation('doc_abc123');
```

---

## 예시 5: 배치 처리

```typescript
import { create as createContact } from './servers/salesforce/contacts/create';
import { read as readSpreadsheet } from './servers/google-drive/spreadsheets/read';

async function batchCreateContacts(spreadsheetId: string) {
  // 1. 스프레드시트 읽기
  const sheet = await readSpreadsheet({
    spreadsheetId,
    range: 'Contacts!A2:E1000'  // 헤더 제외, 최대 1000행
  });
  
  console.log('Processing', sheet.values.length, 'contacts');
  
  // 2. 배치 단위로 처리 (10개씩)
  const batchSize = 10;
  const results = [];
  
  for (let i = 0; i < sheet.values.length; i += batchSize) {
    const batch = sheet.values.slice(i, i + batchSize);
    
    console.log(`Batch ${i / batchSize + 1}: Processing ${batch.length} contacts`);
    
    // 병렬 생성
    const batchResults = await Promise.all(
      batch.map(row => createContact({
        firstName: row[0],
        lastName: row[1],
        email: row[2],
        phone: row[3],
        company: row[4]
      }))
    );
    
    results.push(...batchResults);
    
    // 간단한 통계만 로깅 (전체 데이터는 로깅 안 함)
    console.log(`  ✓ Created ${batchResults.length} contacts`);
    
    // Rate limit 고려
    if (i + batchSize < sheet.values.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  // 최종 통계만 반환
  return {
    total: results.length,
    successful: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length
  };
}

// 실행
const stats = await batchCreateContacts('spreadsheet_xyz');
console.log('Final stats:', stats);
```

---

## 예시 6: Skills로 저장 (재사용)

### 첫 번째 실행 후
```typescript
// skills/syncGoogleDriveToSalesforce.ts 자동 생성
/**
 * Google Drive 스프레드시트를 Salesforce 계정으로 동기화
 * 
 * @param spreadsheetId Google Drive 스프레드시트 ID
 * @param revenueThreshold 최소 매출 기준 (기본값: 50000)
 */
export async function syncGoogleDriveToSalesforce(
  spreadsheetId: string,
  revenueThreshold: number = 50000
) {
  // 이전 예시 3의 코드
  // ...
}
```

### 두 번째 실행 (재사용)
```
사용자: "이번엔 Q4 스프레드시트로 동일 작업해줘"

Claude:
> list skills/
→ syncGoogleDriveToSalesforce.ts ✓

"아, 이전에 만든 스킬이 있네!"

import { syncGoogleDriveToSalesforce } from './skills/syncGoogleDriveToSalesforce';

await syncGoogleDriveToSalesforce('q4_spreadsheet_id');
```

**이점:**
- ✅ 코드 일관성
- ✅ 토큰 절약
- ✅ 빠른 실행

---

## 토큰 사용량 비교

### 시나리오: "Salesforce에서 계정 100개 생성"

#### 기존 방식 (Tool Calling)
```
1. 모든 Salesforce 도구 로드: 8,000 토큰
2. 각 create 호출마다 모델 통과: 100 × 200 = 20,000 토큰
3. 총: 28,000 토큰
```

#### 새 방식 (Code Execution)
```
1. 관련 카테고리만 탐색: 100 토큰
2. create.ts 정의 로드: 200 토큰
3. 코드 생성: 500 토큰
4. 실행 (반복문, 실행 환경에서): 0 토큰
5. 결과 통계만 반환: 50 토큰
6. 총: 850 토큰
```

**절감: 97%** 🎉

---

## 요약

| 특징 | 기존 방식 | Code Execution |
|------|----------|----------------|
| 도구 로딩 | 모두 미리 | 필요한 것만 |
| 중간 데이터 | context 통과 | 실행 환경 내 |
| 반복 작업 | 매번 모델 통과 | 코드로 처리 |
| 토큰 사용 | 매우 높음 | 매우 낮음 |
| 복잡한 로직 | 어려움 | 쉬움 |
| 재사용성 | 낮음 | 높음 (Skills) |

이 프로젝트로 생성된 구조는 이러한 모든 장점을 활용할 수 있게 해줍니다! 🚀
