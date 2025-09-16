from django.core.management.base import BaseCommand
from problems.models import Problem


class Command(BaseCommand):
    help = 'Seed the database with top 100 LeetCode problems'

    def handle(self, *args, **options):
        """Seed the database with top 100 LeetCode problems."""
        
        problems_data = [
            {"id": 1, "title": "Two Sum", "url": "https://leetcode.com/problems/two-sum/", "difficulty": "Easy", "tags": ["Array", "Hash Table", "Amazon", "Google", "Microsoft"]},
            {"id": 2, "title": "Add Two Numbers", "url": "https://leetcode.com/problems/add-two-numbers/", "difficulty": "Medium", "tags": ["Linked List", "Math", "Recursion", "Amazon", "Microsoft"]},
            {"id": 3, "title": "Longest Substring Without Repeating Characters", "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "difficulty": "Medium", "tags": ["Hash Table", "String", "Sliding Window", "Amazon", "Google"]},
            {"id": 4, "title": "Median of Two Sorted Arrays", "url": "https://leetcode.com/problems/median-of-two-sorted-arrays/", "difficulty": "Hard", "tags": ["Array", "Binary Search", "Divide and Conquer", "Google", "Microsoft"]},
            {"id": 5, "title": "Longest Palindromic Substring", "url": "https://leetcode.com/problems/longest-palindromic-substring/", "difficulty": "Medium", "tags": ["String", "Dynamic Programming", "Amazon", "Google"]},
            {"id": 6, "title": "Zigzag Conversion", "url": "https://leetcode.com/problems/zigzag-conversion/", "difficulty": "Medium", "tags": ["String", "Amazon"]},
            {"id": 7, "title": "Reverse Integer", "url": "https://leetcode.com/problems/reverse-integer/", "difficulty": "Medium", "tags": ["Math", "Amazon", "Microsoft"]},
            {"id": 8, "title": "String to Integer (atoi)", "url": "https://leetcode.com/problems/string-to-integer-atoi/", "difficulty": "Medium", "tags": ["String", "Amazon", "Microsoft"]},
            {"id": 9, "title": "Palindrome Number", "url": "https://leetcode.com/problems/palindrome-number/", "difficulty": "Easy", "tags": ["Math", "Amazon", "Google"]},
            {"id": 10, "title": "Regular Expression Matching", "url": "https://leetcode.com/problems/regular-expression-matching/", "difficulty": "Hard", "tags": ["String", "Dynamic Programming", "Recursion", "Google", "Microsoft"]},
            {"id": 11, "title": "Container With Most Water", "url": "https://leetcode.com/problems/container-with-most-water/", "difficulty": "Medium", "tags": ["Array", "Two Pointers", "Greedy", "Amazon", "Google"]},
            {"id": 12, "title": "Integer to Roman", "url": "https://leetcode.com/problems/integer-to-roman/", "difficulty": "Medium", "tags": ["Hash Table", "Math", "String", "Amazon"]},
            {"id": 13, "title": "Roman to Integer", "url": "https://leetcode.com/problems/roman-to-integer/", "difficulty": "Easy", "tags": ["Hash Table", "Math", "String", "Amazon"]},
            {"id": 14, "title": "Longest Common Prefix", "url": "https://leetcode.com/problems/longest-common-prefix/", "difficulty": "Easy", "tags": ["String", "Trie", "Amazon", "Google"]},
            {"id": 15, "title": "3Sum", "url": "https://leetcode.com/problems/3sum/", "difficulty": "Medium", "tags": ["Array", "Two Pointers", "Sorting", "Amazon", "Google", "Microsoft"]},
            {"id": 16, "title": "3Sum Closest", "url": "https://leetcode.com/problems/3sum-closest/", "difficulty": "Medium", "tags": ["Array", "Two Pointers", "Sorting", "Amazon"]},
            {"id": 17, "title": "Letter Combinations of a Phone Number", "url": "https://leetcode.com/problems/letter-combinations-of-a-phone-number/", "difficulty": "Medium", "tags": ["Hash Table", "String", "Backtracking", "Amazon", "Google"]},
            {"id": 18, "title": "4Sum", "url": "https://leetcode.com/problems/4sum/", "difficulty": "Medium", "tags": ["Array", "Two Pointers", "Sorting", "Amazon"]},
            {"id": 19, "title": "Remove Nth Node From End of List", "url": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/", "difficulty": "Medium", "tags": ["Linked List", "Two Pointers", "Amazon", "Google"]},
            {"id": 20, "title": "Valid Parentheses", "url": "https://leetcode.com/problems/valid-parentheses/", "difficulty": "Easy", "tags": ["String", "Stack", "Amazon", "Google", "Microsoft"]},
            {"id": 21, "title": "Merge Two Sorted Lists", "url": "https://leetcode.com/problems/merge-two-sorted-lists/", "difficulty": "Easy", "tags": ["Linked List", "Recursion", "Amazon", "Google", "Microsoft"]},
            {"id": 22, "title": "Generate Parentheses", "url": "https://leetcode.com/problems/generate-parentheses/", "difficulty": "Medium", "tags": ["String", "Dynamic Programming", "Backtracking", "Amazon", "Google"]},
            {"id": 23, "title": "Merge k Sorted Lists", "url": "https://leetcode.com/problems/merge-k-sorted-lists/", "difficulty": "Hard", "tags": ["Linked List", "Divide and Conquer", "Heap (Priority Queue)", "Merge Sort", "Amazon", "Google"]},
            {"id": 24, "title": "Swap Nodes in Pairs", "url": "https://leetcode.com/problems/swap-nodes-in-pairs/", "difficulty": "Medium", "tags": ["Linked List", "Recursion", "Amazon"]},
            {"id": 25, "title": "Reverse Nodes in k-Group", "url": "https://leetcode.com/problems/reverse-nodes-in-k-group/", "difficulty": "Hard", "tags": ["Linked List", "Recursion", "Amazon", "Google"]},
            {"id": 26, "title": "Remove Duplicates from Sorted Array", "url": "https://leetcode.com/problems/remove-duplicates-from-sorted-array/", "difficulty": "Easy", "tags": ["Array", "Two Pointers", "Amazon", "Google"]},
            {"id": 27, "title": "Remove Element", "url": "https://leetcode.com/problems/remove-element/", "difficulty": "Easy", "tags": ["Array", "Two Pointers", "Amazon"]},
            {"id": 28, "title": "Find the Index of the First Occurrence in a String", "url": "https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/", "difficulty": "Easy", "tags": ["Two Pointers", "String", "String Matching", "Amazon", "Google"]},
            {"id": 29, "title": "Divide Two Integers", "url": "https://leetcode.com/problems/divide-two-integers/", "difficulty": "Medium", "tags": ["Math", "Bit Manipulation", "Amazon", "Microsoft"]},
            {"id": 30, "title": "Substring with Concatenation of All Words", "url": "https://leetcode.com/problems/substring-with-concatenation-of-all-words/", "difficulty": "Hard", "tags": ["Hash Table", "String", "Sliding Window", "Amazon", "Meta"]},
            {"id": 31, "title": "Next Permutation", "url": "https://leetcode.com/problems/next-permutation/", "difficulty": "Medium", "tags": ["Array", "Two Pointers", "Amazon", "Google"]},
            {"id": 32, "title": "Longest Valid Parentheses", "url": "https://leetcode.com/problems/longest-valid-parentheses/", "difficulty": "Hard", "tags": ["String", "Dynamic Programming", "Stack", "Amazon", "Meta"]},
            {"id": 33, "title": "Search in Rotated Sorted Array", "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/", "difficulty": "Medium", "tags": ["Array", "Binary Search", "Amazon", "Google", "Microsoft"]},
            {"id": 34, "title": "Find First and Last Position of Element in Sorted Array", "url": "https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/", "difficulty": "Medium", "tags": ["Array", "Binary Search", "Amazon", "Google"]},
            {"id": 35, "title": "Search Insert Position", "url": "https://leetcode.com/problems/search-insert-position/", "difficulty": "Easy", "tags": ["Array", "Binary Search", "Amazon", "Google"]},
            {"id": 36, "title": "Valid Sudoku", "url": "https://leetcode.com/problems/valid-sudoku/", "difficulty": "Medium", "tags": ["Array", "Hash Table", "Matrix"]},
            {"id": 37, "title": "Sudoku Solver", "url": "https://leetcode.com/problems/sudoku-solver/", "difficulty": "Hard", "tags": ["Array", "Backtracking", "Matrix"]},
            {"id": 38, "title": "Count and Say", "url": "https://leetcode.com/problems/count-and-say/", "difficulty": "Medium", "tags": ["String"]},
            {"id": 39, "title": "Combination Sum", "url": "https://leetcode.com/problems/combination-sum/", "difficulty": "Medium", "tags": ["Array", "Backtracking"]},
            {"id": 40, "title": "Combination Sum II", "url": "https://leetcode.com/problems/combination-sum-ii/", "difficulty": "Medium", "tags": ["Array", "Backtracking"]},
            {"id": 41, "title": "First Missing Positive", "url": "https://leetcode.com/problems/first-missing-positive/", "difficulty": "Hard", "tags": ["Array", "Hash Table"]},
            {"id": 42, "title": "Trapping Rain Water", "url": "https://leetcode.com/problems/trapping-rain-water/", "difficulty": "Hard", "tags": ["Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"]},
            {"id": 43, "title": "Multiply Strings", "url": "https://leetcode.com/problems/multiply-strings/", "difficulty": "Medium", "tags": ["Math", "String", "Simulation"]},
            {"id": 44, "title": "Wildcard Matching", "url": "https://leetcode.com/problems/wildcard-matching/", "difficulty": "Hard", "tags": ["String", "Dynamic Programming", "Greedy", "Recursion"]},
            {"id": 45, "title": "Jump Game II", "url": "https://leetcode.com/problems/jump-game-ii/", "difficulty": "Medium", "tags": ["Array", "Dynamic Programming", "Greedy"]},
            {"id": 46, "title": "Permutations", "url": "https://leetcode.com/problems/permutations/", "difficulty": "Medium", "tags": ["Array", "Backtracking"]},
            {"id": 47, "title": "Permutations II", "url": "https://leetcode.com/problems/permutations-ii/", "difficulty": "Medium", "tags": ["Array", "Backtracking"]},
            {"id": 48, "title": "Rotate Image", "url": "https://leetcode.com/problems/rotate-image/", "difficulty": "Medium", "tags": ["Array", "Math", "Matrix"]},
            {"id": 49, "title": "Group Anagrams", "url": "https://leetcode.com/problems/group-anagrams/", "difficulty": "Medium", "tags": ["Array", "Hash Table", "String", "Sorting"]},
            {"id": 50, "title": "Pow(x, n)", "url": "https://leetcode.com/problems/powx-n/", "difficulty": "Medium", "tags": ["Math", "Recursion"]},
            {"id": 51, "title": "N-Queens", "url": "https://leetcode.com/problems/n-queens/", "difficulty": "Hard", "tags": ["Array", "Backtracking"]},
            {"id": 52, "title": "N-Queens II", "url": "https://leetcode.com/problems/n-queens-ii/", "difficulty": "Hard", "tags": ["Backtracking"]},
            {"id": 53, "title": "Maximum Subarray", "url": "https://leetcode.com/problems/maximum-subarray/", "difficulty": "Medium", "tags": ["Array", "Divide and Conquer", "Dynamic Programming"]},
            {"id": 54, "title": "Spiral Matrix", "url": "https://leetcode.com/problems/spiral-matrix/", "difficulty": "Medium", "tags": ["Array", "Matrix", "Simulation"]},
            {"id": 55, "title": "Jump Game", "url": "https://leetcode.com/problems/jump-game/", "difficulty": "Medium", "tags": ["Array", "Dynamic Programming", "Greedy"]},
            {"id": 56, "title": "Merge Intervals", "url": "https://leetcode.com/problems/merge-intervals/", "difficulty": "Medium", "tags": ["Array", "Sorting"]},
            {"id": 57, "title": "Insert Interval", "url": "https://leetcode.com/problems/insert-interval/", "difficulty": "Medium", "tags": ["Array"]},
            {"id": 58, "title": "Length of Last Word", "url": "https://leetcode.com/problems/length-of-last-word/", "difficulty": "Easy", "tags": ["String"]},
            {"id": 59, "title": "Spiral Matrix II", "url": "https://leetcode.com/problems/spiral-matrix-ii/", "difficulty": "Medium", "tags": ["Array", "Matrix", "Simulation"]},
            {"id": 60, "title": "Permutation Sequence", "url": "https://leetcode.com/problems/permutation-sequence/", "difficulty": "Hard", "tags": ["Math", "Backtracking"]},
            {"id": 61, "title": "Rotate List", "url": "https://leetcode.com/problems/rotate-list/", "difficulty": "Medium", "tags": ["Linked List", "Two Pointers"]},
            {"id": 62, "title": "Unique Paths", "url": "https://leetcode.com/problems/unique-paths/", "difficulty": "Medium", "tags": ["Math", "Dynamic Programming", "Combinatorics"]},
            {"id": 63, "title": "Unique Paths II", "url": "https://leetcode.com/problems/unique-paths-ii/", "difficulty": "Medium", "tags": ["Array", "Dynamic Programming", "Matrix"]},
            {"id": 64, "title": "Minimum Path Sum", "url": "https://leetcode.com/problems/minimum-path-sum/", "difficulty": "Medium", "tags": ["Array", "Dynamic Programming", "Matrix"]},
            {"id": 65, "title": "Valid Number", "url": "https://leetcode.com/problems/valid-number/", "difficulty": "Hard", "tags": ["String"]},
            {"id": 66, "title": "Plus One", "url": "https://leetcode.com/problems/plus-one/", "difficulty": "Easy", "tags": ["Array", "Math"]},
            {"id": 67, "title": "Add Binary", "url": "https://leetcode.com/problems/add-binary/", "difficulty": "Easy", "tags": ["Math", "String", "Simulation", "Bit Manipulation"]},
            {"id": 68, "title": "Text Justification", "url": "https://leetcode.com/problems/text-justification/", "difficulty": "Hard", "tags": ["Array", "String", "Simulation"]},
            {"id": 69, "title": "Sqrt(x)", "url": "https://leetcode.com/problems/sqrtx/", "difficulty": "Easy", "tags": ["Math", "Binary Search"]},
            {"id": 70, "title": "Climbing Stairs", "url": "https://leetcode.com/problems/climbing-stairs/", "difficulty": "Easy", "tags": ["Math", "Dynamic Programming", "Memoization"]},
            {"id": 71, "title": "Simplify Path", "url": "https://leetcode.com/problems/simplify-path/", "difficulty": "Medium", "tags": ["String", "Stack"]},
            {"id": 72, "title": "Edit Distance", "url": "https://leetcode.com/problems/edit-distance/", "difficulty": "Hard", "tags": ["String", "Dynamic Programming"]},
            {"id": 73, "title": "Set Matrix Zeroes", "url": "https://leetcode.com/problems/set-matrix-zeroes/", "difficulty": "Medium", "tags": ["Array", "Hash Table", "Matrix"]},
            {"id": 74, "title": "Search a 2D Matrix", "url": "https://leetcode.com/problems/search-a-2d-matrix/", "difficulty": "Medium", "tags": ["Array", "Binary Search", "Matrix"]},
            {"id": 75, "title": "Sort Colors", "url": "https://leetcode.com/problems/sort-colors/", "difficulty": "Medium", "tags": ["Array", "Two Pointers", "Sorting"]},
            {"id": 76, "title": "Minimum Window Substring", "url": "https://leetcode.com/problems/minimum-window-substring/", "difficulty": "Hard", "tags": ["Hash Table", "String", "Sliding Window"]},
            {"id": 77, "title": "Combinations", "url": "https://leetcode.com/problems/combinations/", "difficulty": "Medium", "tags": ["Backtracking"]},
            {"id": 78, "title": "Subsets", "url": "https://leetcode.com/problems/subsets/", "difficulty": "Medium", "tags": ["Array", "Backtracking", "Bit Manipulation"]},
            {"id": 79, "title": "Word Search", "url": "https://leetcode.com/problems/word-search/", "difficulty": "Medium", "tags": ["Array", "Backtracking", "Matrix"]},
            {"id": 80, "title": "Remove Duplicates from Sorted Array II", "url": "https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/", "difficulty": "Medium", "tags": ["Array", "Two Pointers"]},
            {"id": 81, "title": "Search in Rotated Sorted Array II", "url": "https://leetcode.com/problems/search-in-rotated-sorted-array-ii/", "difficulty": "Medium", "tags": ["Array", "Binary Search"]},
            {"id": 82, "title": "Remove Duplicates from Sorted List II", "url": "https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/", "difficulty": "Medium", "tags": ["Linked List", "Two Pointers"]},
            {"id": 83, "title": "Remove Duplicates from Sorted List", "url": "https://leetcode.com/problems/remove-duplicates-from-sorted-list/", "difficulty": "Easy", "tags": ["Linked List"]},
            {"id": 84, "title": "Largest Rectangle in Histogram", "url": "https://leetcode.com/problems/largest-rectangle-in-histogram/", "difficulty": "Hard", "tags": ["Array", "Stack", "Monotonic Stack"]},
            {"id": 85, "title": "Maximal Rectangle", "url": "https://leetcode.com/problems/maximal-rectangle/", "difficulty": "Hard", "tags": ["Array", "Dynamic Programming", "Stack", "Matrix", "Monotonic Stack"]},
            {"id": 86, "title": "Partition List", "url": "https://leetcode.com/problems/partition-list/", "difficulty": "Medium", "tags": ["Linked List", "Two Pointers"]},
            {"id": 87, "title": "Scramble String", "url": "https://leetcode.com/problems/scramble-string/", "difficulty": "Hard", "tags": ["String", "Dynamic Programming"]},
            {"id": 88, "title": "Merge Sorted Array", "url": "https://leetcode.com/problems/merge-sorted-array/", "difficulty": "Easy", "tags": ["Array", "Two Pointers", "Sorting"]},
            {"id": 89, "title": "Gray Code", "url": "https://leetcode.com/problems/gray-code/", "difficulty": "Medium", "tags": ["Math", "Backtracking", "Bit Manipulation"]},
            {"id": 90, "title": "Subsets II", "url": "https://leetcode.com/problems/subsets-ii/", "difficulty": "Medium", "tags": ["Array", "Backtracking", "Bit Manipulation"]},
            {"id": 91, "title": "Decode Ways", "url": "https://leetcode.com/problems/decode-ways/", "difficulty": "Medium", "tags": ["String", "Dynamic Programming"]},
            {"id": 92, "title": "Reverse Linked List II", "url": "https://leetcode.com/problems/reverse-linked-list-ii/", "difficulty": "Medium", "tags": ["Linked List"]},
            {"id": 93, "title": "Restore IP Addresses", "url": "https://leetcode.com/problems/restore-ip-addresses/", "difficulty": "Medium", "tags": ["String", "Backtracking"]},
            {"id": 94, "title": "Binary Tree Inorder Traversal", "url": "https://leetcode.com/problems/binary-tree-inorder-traversal/", "difficulty": "Easy", "tags": ["Stack", "Tree", "Depth-First Search", "Binary Tree"]},
            {"id": 95, "title": "Unique Binary Search Trees II", "url": "https://leetcode.com/problems/unique-binary-search-trees-ii/", "difficulty": "Medium", "tags": ["Dynamic Programming", "Backtracking", "Tree", "Binary Search Tree", "Binary Tree"]},
            {"id": 96, "title": "Unique Binary Search Trees", "url": "https://leetcode.com/problems/unique-binary-search-trees/", "difficulty": "Medium", "tags": ["Math", "Dynamic Programming", "Tree", "Binary Search Tree", "Binary Tree"]},
            {"id": 97, "title": "Interleaving String", "url": "https://leetcode.com/problems/interleaving-string/", "difficulty": "Medium", "tags": ["String", "Dynamic Programming"]},
            {"id": 98, "title": "Validate Binary Search Tree", "url": "https://leetcode.com/problems/validate-binary-search-tree/", "difficulty": "Medium", "tags": ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"]},
            {"id": 99, "title": "Recover Binary Search Tree", "url": "https://leetcode.com/problems/recover-binary-search-tree/", "difficulty": "Medium", "tags": ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"]},
            {"id": 100, "title": "Same Tree", "url": "https://leetcode.com/problems/same-tree/", "difficulty": "Easy", "tags": ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"]},
        ]
        
        created_count = 0
        for problem_data in problems_data:
            problem, created = Problem.objects.get_or_create(
                id=problem_data['id'],
                defaults={
                    'title': problem_data['title'],
                    'url': problem_data['url'],
                    'difficulty': problem_data['difficulty'],
                    'tags': problem_data['tags']
                }
            )
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded {created_count} problems. '
                f'Total problems in database: {Problem.objects.count()}'
            )
        )
