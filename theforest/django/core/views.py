from django.shortcuts import render, redirect
from .forms import FamilyMemberForm
from .decorators import role_required
# Create your views here.

def home(request):
    return render(request, 'core/home.html')

@role_required('parent')


def add_family_member(request):
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST, request.FILES)
        if form.is_valid():
            family_member = form.save()
            parents = form.cleaned_data.get('parents')
            family_member.parents.set(parents)  # Set multiple parents
            return redirect('home')  # Redirect after saving
    else:
        form = FamilyMemberForm()

    return render(request, 'core/add_member.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import FamilyMember

def family_member_profile(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk)
    return render(request, 'core/member_profile.html', {'member': member})


from django.core.serializers.json import DjangoJSONEncoder
import json
def build_tree_node(member):
    node = {
        "text": {
            "name": f"{member.first_name} {member.last_name}",
        },
        "HTMLid": f"user-{member.id}",
        "link": f"/profile/{member.id}/",  # Link to the user's profile page
    }

    if member.photo:
        node["image"] = member.photo.url
    else:
        node["image"] = "/static/img/default-user.png"  # Optional fallback for images

    # Add "View Profile" button at the bottom
    node["button"] = {
        "text": "View Profile",  # Button text
        "link": f"/profile/{member.id}/"  # Button link
    }

    # Now handle the multiple parents relationship
    parents = member.parents.all()  # Get all parents of the member
    if parents.exists():
        node["parents"] = [f"user-{parent.id}" for parent in parents]

    return node

def family_tree(request):
    members = FamilyMember.objects.all()  # Ensure you are getting all members
    nodes = []

    # Build tree nodes dynamically
    for member in members:
        node = build_tree_node(member)
        nodes.append(node)

    # Debugging: Check if all members are being retrieved
    print("Nodes: ", nodes)  # This should list all nodes, including children with multiple parents

    # Find the root member (first member with no parent)
    root_member = next((n for n in nodes if "parents" not in n), None)

    if not root_member:
        print("No root member found. Defaulting to an empty root node.")
        root_member = {
            "text": {"name": "No family data found 😢"},
            "HTMLid": "empty-root"
        }

    # Link children to parents
    for node in nodes:
        if "parents" in node:
            for parent_id in node["parents"]:
                for potential_parent in nodes:
                    if potential_parent["HTMLid"] == parent_id:
                        potential_parent.setdefault("children", []).append(node)
                        break

    # Return the final tree structure to the template
    return render(request, 'core/family_tree.html', {
        "tree_data": json.dumps(root_member, cls=DjangoJSONEncoder)
    })
