    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        ans = []
        def bt(nums, new_target, path):
            if new_target < 0: 
                return
            if new_target == 0: 
                ans.append(path[:])
                return
            for i in range(len(nums)):
                bt(nums[i:], new_target - nums[i], path+[nums[i]])
        bt(candidates, target, [])
        return ans


    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        ret = []
        def bt(nums, new_target, path):
            if new_target < 0:
                return 
            if new_target == 0:
                ret.append(path[:])
                return
            for i in range(len(nums)):
                if nums[i] == nums[i-1]and i > 0:
                    continue
                bt(nums[i+1:], new_target - nums[i], path+[nums[i]])
        bt(candidates, target, [])
        return ret
        

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        ans,counter = [], Counter(nums)
        def bt(arr):
            if len(arr) == len(nums):
                ans.append(arr[:])
                return
            for n in counter:
                if counter[n]>0:
                    arr.append(n)
                    counter[n] -= 1
                    bt(arr)
                    arr.pop()
                    counter[n] +=1
        bt([])
        return ans


Permutations with Repetition = n**r
Combination with Repetition = (n+r-1)!/(n-r)!r!
Permutations without Repetition = n!/(n-r)!
Combination without Repetition = n!/(n-r)!r!


    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        ans = set()
        if len(nums)<4: return []
        nums.sort()
        for i in range(len(nums)):
            for j in range(i+1,len(nums)):
                l, r = j+1, len(nums)-1
                while l<r:
                    s = nums[i] + nums[j] + nums[l] + nums[r]
                    if s == target:
                        ans.add((nums[i], nums[j], nums[l], nums[r]))
                        l +=1
                        r -= 1
                    elif s < target:
                        l +=1
                    else:
                        r -= 1
        return ans

    
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        ans = set()
        if len(nums)<3: return []
        nums.sort()
        for i in range(len(nums)):
                l, r = i+1, len(nums)-1
                while l<r:
                    s = nums[i] + nums[l] + nums[r]
                    if s == 0:
                        ans.add((nums[i], nums[l], nums[r]))
                        l +=1
                        r -= 1
                    elif s < 0:
                        l +=1
                    else:
                        r -= 1
        return ans


    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        ans = nums[0] + nums[1] + nums[2]
        for i in range(len(nums)):
            l, r = i+1, len(nums)-1
            while l<r:
                s = nums[i] + nums[l] + nums[r]
                if abs(target-s) < abs(target-ans):
                    ans = s
                    # l += 1 These lines will cause issue ...
                    # r -= 1 increment/decrement will be taken care in next iteration
                elif s > target:
                    r -= 1
                elif s< target:
                    l += 1
                else:
                    return s
        return ans


    def subarraySum(self, nums: List[int], k: int) -> int:
        ps, d, ans =0, {0:1}, 0
        for n in nums:
            ps += n
            if ps -k in d:
                ans = ans + d[ps-k]
            d[ps] = d.get(ps, 0) + 1
        return ans
